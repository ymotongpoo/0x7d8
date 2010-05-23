let map f l = List.rev (List.rev_map f l);;
let enclose x = "(" ^ x ^ ")";;
let cross lhs rhs =
  let rec cross_aux accu = function
    | [] -> accu
    | x::xs -> cross_aux (List.fold_left (fun a y -> (x^y)::a) accu rhs) xs
  in
  cross_aux [] lhs
;;

let rec solution = function
  | 0 -> []
  | n when n < 0 -> prerr_int n; invalid_arg "solution"
  | n -> List.rev_append (atomic n) (separate n)
and atomic = function 
  | 1 -> ["()"]
  | n -> map enclose (solution (n-1)) 
and separate n =
  let rec separate_aux accu = function
    | 0 -> accu
    | k -> separate_aux (List.rev_append (cross (atomic k) (solution (n-k))) accu) (pred k)
  in
  separate_aux [] (n-1)
;;

let test () =
    (* List.map (fun x -> Printf.printf "%s, %!" x) (solution 3); *)
    Printf.printf "%d\n%!" (List.length (solution 14));
;;

test ();;
