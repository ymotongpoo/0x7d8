open Printf

(* Exercise 3 *)
let geo_mean x y = sqrt (x *. y);;

Printf.printf "%f\n" (geo_mean 5.0 10.0);;

(* Exercise 4 *)
let prodMatVec ((x1, y1), (x2, y2)) (x3, y3) = (x1*.x3+.x2*.y3, y1*.x3+.y2*.y3);;

let print_vec (a1, a2) = 
  Printf.printf "(%f, %f)\n" a1 a2;;

print_vec (prodMatVec ((1.0, 2.0), (3.0, 4.0)) (5.0, 6.0));;

