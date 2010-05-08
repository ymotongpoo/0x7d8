let pow x n =
  let rec pow ret = function
    | 0 -> ret
    | n -> pow (x*ret) (n-1)
  in
  pow 1 n
;;

let filename = "A-large.in";;

let state n k = if k mod (pow 2 n) = (pow 2 n) - 1 then "ON" else "OFF"

let print_state line state = 
  Printf.printf "Case #%d: %s\n" line state
;;

let test filname =
  let input = open_in filename in
  try
    let nline = int_of_string (input_line input) in
    for i = 1 to nline do
      let str =  input_line input in
      print_state i (Scanf.sscanf str "%d %d" (fun x y -> state x y));
    done;
  with
    End_of_file -> 
      close_in input
;;

test filename;;
