load harness

@test "medium-1" {
  check 'a := 98 ; b := 76 ; while ¬ ( a = b ) do { if a < b then b := b - a else a := a - b }' '{a → 2, b → 2}'
}

@test "medium-2" {
  check 'a := 369 ; b := 1107 ; while ¬ ( a = b ) do { if a < b then b := b - a else a := a - b }' '{a → 369, b → 369}'
}

@test "medium-3" {
  check 'a := 369 ; b := 1108 ; while ¬ ( a = b ) do { if a < b then b := b - a else a := a - b }' '{a → 1, b → 1}'
}

@test "medium-4" {
  check 'i := 5 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }' '{fact → 120, i → 0}'
}

@test "medium-5" {
  check 'i := 3 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }' '{fact → 6, i → 0}'
}

@test "medium-6" {
  check 'i := -1 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }' '{fact → 1, i → -1}'
}

@test "medium-7" {
  check 'while false do x := 1 ; if true then y := 1 else z := 1' '{y → 1}'
}

@test "medium-8" {
  check 'while false do x := 1 ; y := 1' '{y → 1}'
}

@test "medium-9" {
  check 'if false then kj := 12 else while false do l0 := 0' '{}'
}

@test "medium-10" {
  check 'if false then while true do skip else x := 2' '{x → 2}'
}

@test "medium-11" {
  check 'i := 5 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }' '{fact → 120, i → 0}'
}

@test "medium-12" {
  check 'i := 3 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }' '{fact → 6, i → 0}'
}

@test "medium-13" {
  check 'i := -1 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }' '{fact → 1, i → -1}'
}

@test "medium-14" {
  check 'while false do x := 1 ; if true then y := 1 else z := 1' '{y → 1}'
}

@test "medium-15" {
  check 'while false do x := 1 ; y := 1' '{y → 1}'
}