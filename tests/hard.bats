load harness

@test "hard-1" {
  check 'if true ∧ -3 < 4 then x := -1 else y := 2' '{x → -1}'
}

@test "hard-2" {
  check 'if ( 1 - 1 ) < 0 then z8 := 09 else z3 := 90' '{z3 → 90}'
}

@test "hard-3" {
  check 'z := ( x8 + 1 ) * -4' '{z → -4}'
}

@test "hard-4" {
  check 'x := y - -2' '{x → 2}'
}

@test "hard-5" {
  check 'while 0 = z * -4 do z := -1' '{z → -1}'
}

@test "hard-6" {
  check 'if 3 < -3 then g := 3 + -2 else h := 09 + 90' '{h → 99}'
}

@test "hard-7" {
  check 'if ¬ true then x := 1 else Y := 1' '{Y → 1}'
}

@test "hard-8" {
  check 'if ( true ) then x := 1 else zir9 := 2' '{x → 1}'
}

@test "hard-9" {
  check 'if -1 < -2 then g40 := 40 else g41 := 14' '{g41 → 14}'
}

@test "hard-10" {
  check 'if ( true ∧ true ) then p := t else p := t + 1' '{p → 0}'
}

@test "hard-11" {
  check 'if ( true ∨ -1 < 0 ) then k := ( 49 ) * 3 + k else k := 2 * 2 * 2 + 3' '{k → 147}'
}

@test "hard-12" {
  check 'if ( y < z ) then g := 3 else gh := 2' '{gh → 2}'
}

@test "hard-13" {
  check 'if ( true ∨ true ) then x := z + y else x := y + 1 ; skip' '{x → 0}'
}

@test "hard-14" {
  check 'while z * x = -3 ∧ 3 * x = z + R do z := y * z ; y := 1 - 0' '{y → 1}'
}

@test "hard-15" {
  check 'if ( y * 4 < -1 - x ∧ -1 = 0 + y ) then z := ( -1 - -1 ) * -4 else z := 2 * -4 ; if ( y - -3 = y * z ∨ n * y < 1 * 2 ) then skip else if ( 1 < 0 - x ∨ true ) then x := y + -4 else y := -4 * y' '{z → -8}'
}


@test "hard-16" {
  check 'if ( false ∨ 3 < y + X ) then l := lv + -1 else x := -4 - z ; while -1 - p = 2 - -3 ∧ false do while ( ¬ ( 2 * -2 < y * y ) ) do skip' '{x → -4}'
}

@test "hard-17" {
  check 'while ( ¬ ( 0 - -1 < 2 + z ) ) do skip ; while -1 * IY = 2 - L ∧ 0 + x < 2 + 2 do while ( ¬ ( z + S = z - -1 ) ) do if ( false ∨ NT + -3 = 3 ) then y := k * 0 else y := 0 - y' '{}'
}

@test "hard-18" {
  check 'if ( z - 2 < -2 ∧ y * -1 < z * 2 ) then while ( ¬ ( 2 * z < y + y ) ) do skip else while H + z = 0 - -2 ∧ -2 * 0 < 3 - X do skip' '{}'
}
