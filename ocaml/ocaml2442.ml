open Printf

let is_lowercase c =
  let n = int_of_char c in
  if n >= 97 && n <= 122 then
    true
  else
    false
;;

let capitalize c =
  if is_lowercase c then
    let c_ = (int_of_char c) - 32 in
    char_of_int c_
  else
    c
;;


let uppercase str =
  let len = String.length str in
  let ret = String.make len '0' in
  begin
    for i = 0 to len - 1 do
      let c = str.[i] in
      ret.[i] <- (capitalize c)
    done;
  end
	ret
;;


Printf.printf "%s\n" (uppercase "abcdEFG");;
