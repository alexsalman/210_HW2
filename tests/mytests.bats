load harness

@test "mytest-1" {
  check 'while false do x := 1 ; array := [1, -23, 101, -7]' '{array → [1, -23, 101, -7]}'
}

@test "mytest-2" {
  check 'if false then while true do skip else x := [23, 500000]' '{x → [23, 500000]}'
}

@test "mytest-3" {
  check 'if ( true ) then x35 := [-237] else zir9 := 2' '{x35 → [-237]}'
}

@test "mytest-4" {
  check 'if ( 1 - 1 ) < 0 then z8 := 09 else z3 := [04,20,90]' '{z3 → [4, 20, 90]}'
}

@test "mytest-5" {
  check 'if ( [1,2,3,5,5,5,5,5] < [1,2,3,-20,79] ) then k := ( 49 ) * 3 + k else k := 2 * 2 * 2 + 3' '{k → 11}'
}
