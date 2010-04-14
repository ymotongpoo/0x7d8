(* -*- coding: utf-8 -*-; *)
(*
type 'a t
type 'a elt

val create : unit -> 'a t
(** create a dlist *)

val is_empty : 'a t -> bool
(** empty check *)

val length : 'a t -> int
(** O(1) *)

val add : 'a t -> 'a -> 'a elt
(** O(1) : [add t v] adds a value [v] at the end of [t],
  then returns its slot *)

val remove : 'a t -> 'a elt -> [ `Ok | `Already_removed ]
(** O(1) : [remove t elt] removes a slot [elt] from [t] *)

val value : 'a elt -> 'a
(** [value elt] returns the value from a slot [elt] *)

val take_hd : 'a t -> 'a option
(** [take_hd t] returns the first value of [t].
  If [t] is empty, returns [None] *)
(** O(1) : 
  If [t] is not empty, [take_hd t] removes the first slot
  from the list and returns [Some v], where [v] is the value of
  the slot.

  If [t] is empty, it returns [None] *)

http://en.wikipedia.org/wiki/Doubly-linked_list
*)

type 'a elt = { data: 'a; mutable prev: 'a elt option; mutable next: 'a elt option; }

type 'a t = { 
  mutable nelem: int;
  mutable first: 'a elt option;
  mutable last: 'a elt option;
}

let create () = {nelem = 0; first = None; last = None};;

let is_empty t = t = {nelem = 0; first = None; last = None };;
  
let length t = t.nelem;;
  
let add t v =
  let x = { data = v; prev = t.last; next = None} in
  if is_empty t then 
    begin
      t.nelem <- t.nelem + 1;
      t.first <- Some x;
      t.last  <- Some x;
      t
    end
  else
    begin
      t.nelem <- t.nelem + 1;
      t.last  <- Some x;
      t;
    end
;;
  
