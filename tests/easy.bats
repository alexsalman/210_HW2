load harness

@test "easy-1" {
  check 'x := 1' '{x → 1}'
}

@test "easy-2" {
  check 'skip' '{}'
}

@test "easy-3" {
  check 'if true then x := 1 else x := 0' '{x → 1}'
}

@test "easy-4" {
  check 'while false do x := 3' '{}'
}

@test "easy-5" {
  check 'while x = 0 do x := 3' '{x → 3}'
}

@test "easy-6" {
  check 'x := 1 * 9 ; if 5 < x then x := 2 - 2 else y := 9' '{x → 0}'
}

@test "easy-7" {
  check 'if x = 0 ∧ y < 4 then x := 1 else x := 3' '{x → 1}'
}

@test "easy-8" {
  check 'if x = 0 ∧ 4 < 4 then x := 1 else x := 3' '{x → 3}'
}

@test "easy-9" {
  check 'if 0 < x ∧ 4 = 4 then x := 1 else x := 3' '{x → 3}'
}

@test "easy-10" {
  check 'if 0 < x ∧ 4 < y then x := 1 else x := 3' '{x → 3}'
}

@test "easy-11" {
  check 'if x = 0 ∨ y < 4 then x := 1 else x := 3' '{x → 1}'
}

@test "easy-12" {
  check 'if x = 0 ∨ 4 < 4 then x := 1 else x := 3' '{x → 1}'
}

@test "easy-13" {
  check 'if 0 < x ∨ 4 = 4 then x := 1 else x := 3' '{x → 1}'
}

@test "easy-14" {
  check 'if 0 < x ∨ 4 < y then x := 1 else x := 3' '{x → 3}'
}

@test "easy-15" {
  check 'while ¬ true do x := 1' '{}'
}

@test "easy-16" {
  check 'while ¬ ( x < 0 ) do x := -1' '{x → -1}'
}

@test "easy-17" {
  check 'TRUE := 1' '{TRUE → 1}'
}

@test "easy-18" {
  check 'FALSE := 1' '{FALSE → 1}'
}