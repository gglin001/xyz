// TODO: support `-o -`
// TODO: support `lit`
// RUN: xyz.mlir_strip_debuginfo %s

#loc = loc("triton-xyz/debug/test_vec_add.py":10:0)
#loc15 = loc("x_ptr"(#loc))
#loc16 = loc("y_ptr"(#loc))
#loc17 = loc("output_ptr"(#loc))
#loc18 = loc("n_elements"(#loc))
module {
  tt.func public @add_kernel(%x_ptr: !tt.ptr<f32> {tt.divisibility = 16 : i32} loc("x_ptr"(#loc)), %y_ptr: !tt.ptr<f32> {tt.divisibility = 16 : i32} loc("y_ptr"(#loc)), %output_ptr: !tt.ptr<f32> {tt.divisibility = 16 : i32} loc("output_ptr"(#loc)), %n_elements: i32 {tt.divisibility = 16 : i32} loc("n_elements"(#loc))) attributes {noinline = false} {
    %block_start = arith.constant 8192 : i64 loc(#loc19)
    %offsets = arith.constant dense<-2147483648> : tensor<8192xi64> loc(#loc20)
    %offsets_0 = arith.constant dense<2147483647> : tensor<8192xi64> loc(#loc20)
    %c-2147483648_i64 = arith.constant -2147483648 : i64 loc(#loc3)
    %c2147483647_i64 = arith.constant 2147483647 : i64 loc(#loc3)
    %c8192_i32 = arith.constant 8192 : i32 loc(#loc3)
    %pid = tt.get_program_id x : i32 loc(#loc21)
    %block_start_1 = arith.extsi %pid : i32 to i64 loc(#loc19)
    %block_start_2 = arith.muli %block_start_1, %block_start : i64 loc(#loc19)
    %block_start_3 = arith.cmpi sle, %block_start_2, %c2147483647_i64 : i64 loc(#loc19)
    %block_start_4 = arith.cmpi sge, %block_start_2, %c-2147483648_i64 : i64 loc(#loc19)
    %block_start_5 = arith.andi %block_start_3, %block_start_4 : i1 loc(#loc19)
    tt.assert %block_start_5, "int32 overflow detected for operation mul" : i1 loc(#loc19)
    %block_start_6 = arith.muli %pid, %c8192_i32 : i32 loc(#loc19)
    %offsets_7 = tt.make_range {end = 8192 : i32, start = 0 : i32} : tensor<8192xi32> loc(#loc22)
    %offsets_8 = tt.splat %block_start_6 : i32 -> tensor<8192xi32> loc(#loc20)
    %offsets_9 = arith.extsi %offsets_8 : tensor<8192xi32> to tensor<8192xi64> loc(#loc20)
    %offsets_10 = arith.extsi %offsets_7 : tensor<8192xi32> to tensor<8192xi64> loc(#loc20)
    %offsets_11 = arith.addi %offsets_9, %offsets_10 : tensor<8192xi64> loc(#loc20)
    %offsets_12 = arith.cmpi sle, %offsets_11, %offsets_0 : tensor<8192xi64> loc(#loc20)
    %offsets_13 = arith.cmpi sge, %offsets_11, %offsets : tensor<8192xi64> loc(#loc20)
    %offsets_14 = arith.andi %offsets_12, %offsets_13 : tensor<8192xi1> loc(#loc20)
    tt.assert %offsets_14, "int32 overflow detected for operation add" : tensor<8192xi1> loc(#loc20)
    %offsets_15 = arith.addi %offsets_8, %offsets_7 : tensor<8192xi32> loc(#loc20)
    %mask = tt.splat %n_elements : i32 -> tensor<8192xi32> loc(#loc23)
    %mask_16 = arith.cmpi slt, %offsets_15, %mask : tensor<8192xi32> loc(#loc23)
    %x = tt.splat %x_ptr : !tt.ptr<f32> -> tensor<8192x!tt.ptr<f32>> loc(#loc24)
    %x_17 = tt.addptr %x, %offsets_15 : tensor<8192x!tt.ptr<f32>>, tensor<8192xi32> loc(#loc24)
    %x_18 = tt.load %x_17, %mask_16 : tensor<8192x!tt.ptr<f32>> loc(#loc25)
    %y = tt.splat %y_ptr : !tt.ptr<f32> -> tensor<8192x!tt.ptr<f32>> loc(#loc26)
    %y_19 = tt.addptr %y, %offsets_15 : tensor<8192x!tt.ptr<f32>>, tensor<8192xi32> loc(#loc26)
    %y_20 = tt.load %y_19, %mask_16 : tensor<8192x!tt.ptr<f32>> loc(#loc27)
    %output = arith.addf %x_18, %y_20 : tensor<8192xf32> loc(#loc28)
    %0 = tt.splat %output_ptr : !tt.ptr<f32> -> tensor<8192x!tt.ptr<f32>> loc(#loc12)
    %1 = tt.addptr %0, %offsets_15 : tensor<8192x!tt.ptr<f32>>, tensor<8192xi32> loc(#loc12)
    tt.store %1, %output, %mask_16 : tensor<8192x!tt.ptr<f32>> loc(#loc13)
    tt.return loc(#loc14)
  } loc(#loc)
} loc(#loc)
#loc1 = loc("triton-xyz/debug/test_vec_add.py":25:24)
#loc2 = loc("triton-xyz/debug/test_vec_add.py":26:28)
#loc3 = loc(unknown)
#loc4 = loc("triton-xyz/debug/test_vec_add.py":20:24)
#loc5 = loc("triton-xyz/debug/test_vec_add.py":26:41)
#loc6 = loc("triton-xyz/debug/test_vec_add.py":28:21)
#loc7 = loc("triton-xyz/debug/test_vec_add.py":31:24)
#loc8 = loc("triton-xyz/debug/test_vec_add.py":31:16)
#loc9 = loc("triton-xyz/debug/test_vec_add.py":32:24)
#loc10 = loc("triton-xyz/debug/test_vec_add.py":32:16)
#loc11 = loc("triton-xyz/debug/test_vec_add.py":33:17)
#loc12 = loc("triton-xyz/debug/test_vec_add.py":35:26)
#loc13 = loc("triton-xyz/debug/test_vec_add.py":35:35)
#loc14 = loc("triton-xyz/debug/test_vec_add.py":35:4)
#loc19 = loc("block_start"(#loc1))
#loc20 = loc("offsets"(#loc2))
#loc21 = loc("pid"(#loc4))
#loc22 = loc("offsets"(#loc5))
#loc23 = loc("mask"(#loc6))
#loc24 = loc("x"(#loc7))
#loc25 = loc("x"(#loc8))
#loc26 = loc("y"(#loc9))
#loc27 = loc("y"(#loc10))
#loc28 = loc("output"(#loc11))

// module {
//   tt.func public @add_kernel(%x_ptr: !tt.ptr<f32> {tt.divisibility = 16 : i32}, %y_ptr: !tt.ptr<f32> {tt.divisibility = 16 : i32}, %output_ptr: !tt.ptr<f32> {tt.divisibility = 16 : i32}, %n_elements: i32 {tt.divisibility = 16 : i32}) attributes {noinline = false} {
//     %block_start = arith.constant 8192 : i64
//     %offsets = arith.constant dense<-2147483648> : tensor<8192xi64>
//     %offsets_0 = arith.constant dense<2147483647> : tensor<8192xi64>
//     %c-2147483648_i64 = arith.constant -2147483648 : i64
//     %c2147483647_i64 = arith.constant 2147483647 : i64
//     %c8192_i32 = arith.constant 8192 : i32
//     %pid = tt.get_program_id x : i32
//     %block_start_1 = arith.extsi %pid : i32 to i64
//     %block_start_2 = arith.muli %block_start_1, %block_start : i64
//     %block_start_3 = arith.cmpi sle, %block_start_2, %c2147483647_i64 : i64
//     %block_start_4 = arith.cmpi sge, %block_start_2, %c-2147483648_i64 : i64
//     %block_start_5 = arith.andi %block_start_3, %block_start_4 : i1
//     tt.assert %block_start_5, "int32 overflow detected for operation mul" : i1
//     %block_start_6 = arith.muli %pid, %c8192_i32 : i32
//     %offsets_7 = tt.make_range {end = 8192 : i32, start = 0 : i32} : tensor<8192xi32>
//     %offsets_8 = tt.splat %block_start_6 : i32 -> tensor<8192xi32>
//     %offsets_9 = arith.extsi %offsets_8 : tensor<8192xi32> to tensor<8192xi64>
//     %offsets_10 = arith.extsi %offsets_7 : tensor<8192xi32> to tensor<8192xi64>
//     %offsets_11 = arith.addi %offsets_9, %offsets_10 : tensor<8192xi64>
//     %offsets_12 = arith.cmpi sle, %offsets_11, %offsets_0 : tensor<8192xi64>
//     %offsets_13 = arith.cmpi sge, %offsets_11, %offsets : tensor<8192xi64>
//     %offsets_14 = arith.andi %offsets_12, %offsets_13 : tensor<8192xi1>
//     tt.assert %offsets_14, "int32 overflow detected for operation add" : tensor<8192xi1>
//     %offsets_15 = arith.addi %offsets_8, %offsets_7 : tensor<8192xi32>
//     %mask = tt.splat %n_elements : i32 -> tensor<8192xi32>
//     %mask_16 = arith.cmpi slt, %offsets_15, %mask : tensor<8192xi32>
//     %x = tt.splat %x_ptr : !tt.ptr<f32> -> tensor<8192x!tt.ptr<f32>>
//     %x_17 = tt.addptr %x, %offsets_15 : tensor<8192x!tt.ptr<f32>>, tensor<8192xi32>
//     %x_18 = tt.load %x_17, %mask_16 : tensor<8192x!tt.ptr<f32>>
//     %y = tt.splat %y_ptr : !tt.ptr<f32> -> tensor<8192x!tt.ptr<f32>>
//     %y_19 = tt.addptr %y, %offsets_15 : tensor<8192x!tt.ptr<f32>>, tensor<8192xi32>
//     %y_20 = tt.load %y_19, %mask_16 : tensor<8192x!tt.ptr<f32>>
//     %output = arith.addf %x_18, %y_20 : tensor<8192xf32>
//     %0 = tt.splat %output_ptr : !tt.ptr<f32> -> tensor<8192x!tt.ptr<f32>>
//     %1 = tt.addptr %0, %offsets_15 : tensor<8192x!tt.ptr<f32>>, tensor<8192xi32>
//     tt.store %1, %output, %mask_16 : tensor<8192x!tt.ptr<f32>>
//     tt.return
//   }
// }
