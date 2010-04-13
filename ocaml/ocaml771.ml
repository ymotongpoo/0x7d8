(* -*- coding: utf-8 -*-; *)

(* Exercise 1 *)

type 'a ref = { mutable contents : 'a };;

let ref' x = { contents = x };;
let ex x = x.contents;;
let subst x y = x.contents <- y;;


(* Exercise 2 *)
let incr x = x := (!x + 1);;


(* Exercise 3 *)
let f = ref (fun y -> y+1)
let funny_fact x =
  if x = 1 then 1
  else x * (!f (x-1))
;;

f := funny_fact;;
(* f = ref funny_fact となっているので !f = funny_fact *)
funny_fact 5;;


(* Exercise 4 *)
let fact_imp n =
  let i = ref n and res = ref 1 in
  while (!i <> 0) do
    res := !res * !i;
    i := !i - 1;
  done;
  !res
;;


(* Exercise 5 *)
let fact = function
  | n when n < 0 -> raise (Invalid_argument (string_of_int n))
  | n -> fact_imp n
;;


(* Exercise 7 *)
(*
type color = Blue | Red | Green | White;;
type cpointI = 
    {cget: unit -> int;
     cset: int -> unit;
     cinc: unit -> unit;
     getcolor: unit -> color};;

type pointI =
    {get: unit -> int;
     set: int -> unit;
     inc: unit -> unit;};;

let pointC x this () =
  {get = (fun () -> !x);
   set = (fun newx -> x := newx);
   inc = (fun () -> (this ()).set ((this ()).get () + 1))}
;;

let new_point x =
  let x = ref x in
  let rec this () = pointC x this () in
  this ()
;;

let cpointC x col =
  let rec x = ref x in
  let rec this () =
    {cget = super.get;
     cset = (fun x -> super.set x; col := White);
     cinc = super.inc;
     getcolor = (fun () -> !col)}
  in
  this ()
;;
*)

(* Exercise 9 *)
(*
pervasives.mliを参照

val stdout : out_channel
(** The standard output for the process. *)

val output_string : out_channel -> string -> unit
(** Write the string on the given output channel. *)
*)
let print_int' = output_string stdout string_of_int;;

(* Exercise 10 *)
let cp fromfn tofn = hoge;;
