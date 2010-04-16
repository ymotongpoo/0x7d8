(* doubly linked list *)

module type S = sig

  type 'a t
    (** The type of the dllist *)

  type 'a node
    (** The type of the dllist node *)

  val create : unit -> 'a t
    (** Create an empty dllist *)

  val length : 'a t -> int
    (** O(1). The length of the dllist *)

  val is_empty : 'a t -> bool

  val list : 'a node -> 'a t option
    (** [list node] returns [Some t] if [node] is an element of [t].
        If [node] is removed, it returns [None]. *)

  val is_removed : 'a node -> bool

  val value : 'a node -> 'a
    (** Get the value from the node *)    

  val add : 'a t -> 'a -> 'a node
    (** O(1). [add t v] adds [v] to dllist [t] and returns the newly created
        node for [v]. The node is used to remove the value from [t] in constant
        time.
    *)

  val remove : 'a node -> [ `Already_removed | `Ok | `Fault]
    (** O(1). [remove node] removes [node] from the dllist it belongs to.
        Successful removal returns [`Ok]. If the node is already removed,
        [remove node] returns [`Already_removed]. 
    *)

  val hd : 'a t -> 'a node option
    (** [hd t] returns the first node of the dllist [t]. *)

  val iter : f:('a node -> unit) -> 'a t -> unit
    (** Iteration over the nodes of a dllist from the top to the bottom *)

  val fold : f:('a -> 'b node -> 'a) -> init:'a -> 'b t -> 'a
    (** Folding the nodes of a dllist from the top to the bottom *)

  val fold_rev : f:('a -> 'b node -> 'a) -> init:'a -> 'b t -> 'a
    (** Folding the nodes of a dllist from the bottom to top *)

  (** list <=> dllist conversion functions *)    
  val to_nodes : 'a t -> 'a node list
  val to_list : 'a t -> 'a list
  val of_list : 'a list -> 'a t
  val invariant : 'a t -> unit
    (** Invariant checks *)

  (** validation functions *)
  val hello : unit -> unit
  val show_intt : int t -> unit

end 

module Z : S = struct
  type 'a t = {
    mutable nnode: int;
    mutable first: 'a node option;
    mutable last:  'a node option;
  }
  and 'a node = {
    mutable dll: 'a t option;
    data: 'a;
    mutable prev: 'a node option;
    mutable next: 'a node option;
  };;

  let create () = {nnode = 0; first = None; last = None;};;

  let length t = t.nnode;;
  
  let is_empty t = t = (create ());;
      
  let list n = n.dll;;

  let is_removed n = n.dll = None;;

  let value n = n.data;;

  let add t v =
    let n = { dll = Some t; data = v; prev = t.last; next = None } in
    match t.last with
    | Some l -> 
        begin
          t.nnode <- t.nnode + 1;
          l.next <- Some n;
          t.last <- Some n;
          n;
        end
    | None ->
        begin
          t.nnode <- t.nnode + 1;
          t.first <- Some n;
          t.last  <- Some n;
          n;
        end
  ;;

  let remove n = 
    match n.dll with
    | None -> `Already_removed
    | Some t ->
        match t.first, t.last with
        | None, _ | _, None -> `Fault
        | Some fst, Some lst ->
            begin
              t.nnode <- t.nnode - 1;
              n.dll <- None;
              let p_ = n.prev and n_ = n.next in
              match p_, n_ with
              | None, None ->
                  if fst <> lst then `Fault
                  else
                    begin
                      t.first <- None;
                      t.last  <- None;
                      `Ok
                    end;
              | Some p', None ->
                  if n <> lst then `Fault
                  else
                    begin
                      t.last  <- Some p';
                      p'.next <- None;
                      `Ok;
                    end;
              | None, Some n' ->
                  if n <> fst then `Fault
                  else
                    begin
                      t.first <- Some n';
                      n'.prev <- None;
                      `Ok;
                    end;
              | Some p', Some n' ->
                  begin
                    p'.next <- Some n';
                    n'.prev <- Some p';
                    `Ok
                  end;
            end
  ;;
    

  let hd t = t.first;;

  let iter ~f t =
    let rec iter_node ~f = function
      | None -> ()
      | Some n -> 
          begin
            f n;
            iter_node f n.next;
          end
    in
    iter_node f t.first
  ;;

  let fold ~f ~init t =
    let rec fold' ret = function
      | None -> ret
      | Some n -> fold' (f ret n) n.next
    in
    fold' init t.first
  ;;
      
  let fold_rev ~f ~init t =
    let rec fold_rev' ret = function
      | None -> ret
      | Some n -> fold_rev' (f ret n) n.prev
    in
    fold_rev' init t.last
  ;;

  (** list <=> dllist conversion functions *)    
  let to_nodes l = fold ~f:(fun l n -> n :: l) ~init:[] l;;

  let to_list l = fold_rev ~f:(fun l n -> n.data :: l) ~init:[] l;;

  let of_list l =
    let t = create () in
    let rec add_t ret = function
      | [] -> ret
      | x::xs -> 
          let t = add ret x in
          match t.dll with
          | None -> create ()
          | Some t' -> add_t t' xs
    in
    add_t t l
  ;;
    
  let invariant t = ();;

  let hello () = print_string "hello";;
  let show_intt t = iter ~f:(fun n -> print_int (value n)) t;;

end 

module Test(Z:S) = struct

  open Z

  (* to_list . of_list must be idempotent *)
  let () =
    let ints = 
      let rec ints acc = function
        | 0 -> acc
        | n -> ints (n::acc) (n-1) 
      in
      ints [] 10000
    in
    let t = of_list ints in
    invariant t;
    assert (to_list (of_list ints) = ints)
  ;;
  
  (* random add/removal test *)
  let () =
    let t = create () in
    (* get a random element of a list, one path *)
    let random_in_list = function
      | [] -> None
      | x::xs ->
          let rec random_in_list len cand = function
            | [] -> cand
            | x::xs ->
                (* cand survives : len/(len+1) *)
                (* x overrides : 1/(len+1) *)
                let cand = 
                  if Random.int (len+1) = 0 then x
                  else cand
                in
                random_in_list (len+1) cand xs
          in
          Some (random_in_list 1 x xs)
    in
    let rec loop added rev_current = function
      | 10000 -> rev_current
      | n ->
          invariant t;
          if Random.int 3 = 0 then begin
            let rev_current =
              match random_in_list added with
              | None -> rev_current
              | Some node ->
                  let removed = is_removed node in
                  match removed, remove node with
                  | true, `Already_removed -> rev_current
                  | false, `Ok ->
                      List.filter (fun x -> x != node) rev_current 
                  | _ -> assert false
            in
            loop added rev_current n
          end else 
            let node = add t n in
            loop (node :: added) (node :: rev_current) (n+1)
    in
    let rev_current = loop [] [] 0 in 
    invariant t;
    assert (to_list t = List.rev_map value rev_current);

    (* remove all the elements remaining *)
    let rec f rev_current =
      match random_in_list rev_current with
      | None -> assert (is_empty t)
      | Some node ->
          assert (remove node = `Ok);
          invariant t;
          f (List.filter (fun x -> x != node) rev_current)
    in
    f rev_current
  ;;

  (* misc test *)
  let () = 
    let t = create () in
    assert (is_empty t);
    let ints = [1;2;3;4;5;6;7;8;9;10] in 
    let t = of_list ints in
    let s = ref [] in
    iter t ~f:(fun node -> s := value node :: !s);
    assert (List.rev ints = !s);

    assert (55 = fold t ~init:0 ~f:(fun acc node -> acc + value node));
    assert (ints = fold_rev t ~init:[] ~f:(fun acc node -> value node :: acc))
  ;;

end

module Do_test = Test(Z)
