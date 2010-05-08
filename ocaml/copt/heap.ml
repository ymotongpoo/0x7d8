module Make(O : sig

  type t;;
  val compare : t -> t -> int;;

end) : sig

  type t;;

  val invariant : t -> unit;;
    (** invariant check function *)

  val empty : t;;
  val merge : t -> t -> t;;
  val add : t -> O.t -> t;;
    (** O(log(n)) *)

  val peek_min : t -> O.t option;;
    (** O(1) : [peek_min t] returns [None] if [t] is empty.
        Otherwise, returns the minimum element of [t] *)

  val take_min : t -> (O.t * t) option;;
    (** O(1) : [take_min t] returns [None] if [t] is empty.
        Otherwise, returns the minimum element of [t] and 
        the heap without the minimum element. *)

  val to_list : t -> O.t list;;
  val of_list : O.t list -> t;;

end = struct

  type t = Empty | Heap of int * O.t * t * t;;

  let invariant t = ();;

  let empty = Empty;;

  let merge t1 t2 =
    match t1, t2 with
    | t, Empty | Empty, t -> t
    | Heap (r1, v1, t11, t12), Heap (r2, v2, t21, t22) ->
        if r1 > r2 then Heap (r1+1, v1, t11, t2)
        else Heap (2+1, v2, t21, t1)
  ;;

  let rec add t v =
    match t, v with
    | Heap (r', v', tl, Empty), _ -> 
        let t' = Heap (1, v, Empty, Empty) in
        Heap (r'+1, v', tl, t')
    | Heap (r', v', _, tr), v -> add tr v
    | Empty, _ -> Heap (1, v, Empty, Empty)        
  ;;

  let peek_min = function
    | Empty -> None
    | Heap (r, v, _, _) -> Some v
  ;;

  let take_min = function
    | Empty -> None
    | Heap (r, v, tl, tr) -> Some (v, merge tl tr)
  ;;

  let to_list t = 
    let rec to_list ret = function
      | Empty -> ret
      | Heap (_, v, Empty, Empty) -> v::ret            
      | Heap (_, v, t', Empty) | Heap (_, v, Empty, t') -> 
          to_list (v::ret) t'
      | Heap (_, v, tl', tr') ->
          to_list (v::ret) tl';
          to_list (v::ret) tr';
    in
    to_list [] t
  ;;
      

  let of_list l =
    let rec of_list ret = function
      | [] -> ret
      | x::xs -> of_list (add ret x) xs
    in
    of_list Empty l
  ;;

end


let test () =
  let compare x y = compare (x:int) y in
  let module H = Make(struct type t = int let compare = compare end) in
  let module L = struct
    (* implementation by list. very slow *)
    type t = int list
    let add (t:t) x = List.sort compare (x::t)
    let peek_min = function
      | x::_xs -> Some x
      | _ -> None
    let take_min = function
      | x::xs -> Some (x,xs)
      | _ -> None
    let of_list l = List.sort compare l
    let to_list l = l
  end in
  let rec loop h l = function
    | 0 -> 
        assert (H.to_list h = L.to_list l)
    | n ->
        match Random.int 3 with
    | 0 ->
        assert (H.peek_min h = L.peek_min l);
        begin 
          match H.take_min h, L.take_min l with
          | None, None -> ()
          | Some (x,h), Some (y,l) ->
              assert (x = y);
              loop h l (n-1)
          | _ -> assert false
        end
    | _ ->
        let r = Random.int 1000 in
        let h = H.add h r in
        let l = L.add l r in
        loop h l (n - 1)
  in
  let list =
    let rec iter acc = function
      | 0 -> acc
      | n -> iter (Random.int 1000 :: acc) (n - 1) 
    in
    iter [] 1000
  in
  let h = H.of_list list in
  let l = L.of_list list in
  assert (H.to_list h = L.to_list l);
  loop h l 10000
;;

let () = test (); prerr_endline "Heap test passed" 
