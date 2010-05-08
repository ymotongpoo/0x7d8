module Thunk : sig
  type t = unit -> unit;;
  val run : t -> unit;;
end = struct
  type t = unit -> unit;;
  let run t = t ();;
end

module Ready : sig
  type t;;
  val create : unit -> t;;
  val add : t -> Thunk.t -> unit;;
  val take : t -> Thunk.t option;; (* None if the queue is empty *)
end = struct
  type t = Thunk.t Queue.t;;
  let create () = Queue.create ();;
  let add qt tt = Queue.add tt qt;;
  let take qt = if qt = (create ()) then None else Some (Queue.take qt);;
end

module Scheduler : sig 
  type t;;
  val create : unit -> t;;
  val add : t -> Thunk.t -> unit;;
  val run : t -> unit;;
end = struct
  type t = Ready.t;;
  let create () = Ready.create ();;
  let add st tt = Ready.add st tt;;
  let rec run st = 
    let t = Ready.take st in
    match t with
    | None -> ()
    | Some tt -> 
        begin
          tt ();
          run st;
        end
  ;;
end


let t = Scheduler.create ();;

let cntr = ref 0

let rec incrementer () =
  incr cntr;
  Scheduler.add t incrementer
;;

let rec fizzbuzzer () =
  begin 
    Printf.eprintf "%s\n"
      (match !cntr mod 3, !cntr mod 5 with
      | 0, 0 -> "FizzBuzz"
      | 0, _ -> "Fizz"
      | _, 0 -> "Buzz"
      | _ -> string_of_int !cntr);
  end;
  Scheduler.add t fizzbuzzer
;; 

let () =
  Scheduler.add t incrementer;
  Scheduler.add t fizzbuzzer;
  Scheduler.run t
;; 
