module {
  func.func @matmul_tensors(%arg0: tensor<8x16xi32>, %arg1: tensor<16x32xi32>, %arg2: tensor<8x32xi32>) -> tensor<8x32xi32> {
    %c0 = arith.constant 0 : index
    %c8 = arith.constant 8 : index
    %c32 = arith.constant 32 : index
    %c16 = arith.constant 16 : index
    %c1 = arith.constant 1 : index
    %0 = scf.for %arg3 = %c0 to %c8 step %c1 iter_args(%arg4 = %arg2) -> (tensor<8x32xi32>) {
      %1 = scf.for %arg5 = %c0 to %c32 step %c8 iter_args(%arg6 = %arg4) -> (tensor<8x32xi32>) {
        %2 = scf.for %arg7 = %c0 to %c16 step %c1 iter_args(%arg8 = %arg6) -> (tensor<8x32xi32>) {
          %extracted_slice = tensor.extract_slice %arg0[%arg3, %arg7] [1, 1] [1, 1] : tensor<8x16xi32> to tensor<1x1xi32>
          %extracted_slice_0 = tensor.extract_slice %arg1[%arg7, %arg5] [1, 8] [1, 1] : tensor<16x32xi32> to tensor<1x8xi32>
          %extracted_slice_1 = tensor.extract_slice %arg8[%arg3, %arg5] [1, 8] [1, 1] : tensor<8x32xi32> to tensor<1x8xi32>
          %3 = linalg.matmul ins(%extracted_slice, %extracted_slice_0 : tensor<1x1xi32>, tensor<1x8xi32>) outs(%extracted_slice_1 : tensor<1x8xi32>) -> tensor<1x8xi32>
          %inserted_slice = tensor.insert_slice %3 into %arg8[%arg3, %arg5] [1, 8] [1, 1] : tensor<1x8xi32> into tensor<8x32xi32>
          scf.yield %inserted_slice : tensor<8x32xi32>
        }
        scf.yield %2 : tensor<8x32xi32>
      }
      scf.yield %1 : tensor<8x32xi32>
    }
    return %0 : tensor<8x32xi32>
  }
  module attributes {transform.with_named_sequence} {
    transform.named_sequence @to_tile_forall(%arg0: !transform.any_op {transform.readonly}) {
      %0 = transform.structured.match ops{["linalg.matmul"]} in %arg0 : (!transform.any_op) -> !transform.any_op
      %tiled_op, %forall_op = transform.structured.tile_using_forall %0 tile_sizes [1, 8, 1] : (!transform.any_op) -> (!transform.any_op, !transform.any_op)
      transform.yield
    }
  }
  module attributes {transform.with_named_sequence} {
    transform.named_sequence @to_tile(%arg0: !transform.any_op) {
      %0 = transform.structured.match ops{["linalg.matmul"]} in %arg0 : (!transform.any_op) -> !transform.any_op
      %tiled_linalg_op, %loops:3 = transform.structured.tile_using_for %0 tile_sizes [1, 8, 1] : (!transform.any_op) -> (!transform.any_op, !transform.any_op, !transform.any_op, !transform.any_op)
      transform.yield
    }
  }
  module attributes {transform.with_named_sequence} {
    transform.named_sequence @to_vectorize(%arg0: !transform.any_op) {
      %0 = transform.structured.match ops{["linalg.matmul"]} in %arg0 : (!transform.any_op) -> !transform.any_op
      %tiled_linalg_op, %loops:3 = transform.structured.tile_using_for %0 tile_sizes [1, 8, 1] : (!transform.any_op) -> (!transform.any_op, !transform.any_op, !transform.any_op, !transform.any_op)
      %1 = transform.get_parent_op %tiled_linalg_op {isolated_from_above} : (!transform.any_op) -> !transform.any_op
      %2 = transform.structured.vectorize_children_and_apply_patterns %1 : (!transform.any_op) -> !transform.any_op
      transform.yield
    }
  }
  module attributes {transform.with_named_sequence} {
    transform.named_sequence @__transform_main(%arg0: !transform.any_op {transform.consumed}) {
      %0 = transform.structured.match ops{["linalg.matmul"]} in %arg0 : (!transform.any_op) -> !transform.any_op
      %tiled_linalg_op, %loops:3 = transform.structured.tile_using_for %0 tile_sizes [1, 8, 1] : (!transform.any_op) -> (!transform.any_op, !transform.any_op, !transform.any_op, !transform.any_op)
      %1 = transform.get_parent_op %tiled_linalg_op {isolated_from_above} : (!transform.any_op) -> !transform.any_op
      %2 = transform.structured.vectorize_children_and_apply_patterns %1 : (!transform.any_op) -> !transform.any_op
      %3 = transform.bufferization.one_shot_bufferize layout{IdentityLayoutMap} %arg0 {allow_return_allocs = true, bufferize_function_boundaries = true} : (!transform.any_op) -> !transform.any_op
      %4 = transform.structured.match ops{["func.func"]} in %3 : (!transform.any_op) -> !transform.any_op
      transform.apply_patterns to %4 {
        transform.apply_patterns.vector.lower_contraction
        transform.apply_patterns.vector.lower_outerproduct
      } : !transform.any_op
      transform.apply_patterns to %4 {
        transform.apply_patterns.vector.transfer_to_scf full_unroll = true
      } : !transform.any_op
      transform.yield
    }
  }
}

