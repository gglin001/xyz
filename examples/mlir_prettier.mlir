module {
  func.func @const_16xi32() -> vector<16xi32> {
    %cst = arith.constant dense<[1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1]> : vector<16xi32>
    return %cst : vector<16xi32>
  }
  func.func @main() {
    %0 = call @const_16xi32() : () -> vector<16xi32>
    %1 = arith.addi %0, %0 : vector<16xi32>
    return
  }
}

// xyz.mlir_prettier -t 16 examples/data/example.mlir
//
// module {
//   func.func @const_16xi32() -> vector<16xi32> {
//     %cst = arith.constant dense<1> : vector<16xi32> // NOTE: xyz.mlir_prettier applied
//     return %cst : vector<16xi32>
//   }
//   func.func @main() {
//     %0 = call @const_16xi32() : () -> vector<16xi32>
//     %1 = arith.addi %0, %0 : vector<16xi32>
//     return
//   }
// }
