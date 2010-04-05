open Printf

let rate = 111.12;;

let usd_to_jpy usd = 
  let jpy_base = floor (usd *. rate + 0.5) in 
  int_of_float jpy_base
;;

let jpy_to_usd jpy =
  floor (float_of_int jpy *. 10.0 /. rate) /. 10.0
;;

let print_usd_to_jpy usd =
  let jpy_str = string_of_int (usd_to_jpy usd) in
  Printf.printf "%s dollars are %s yen\n" (string_of_float usd) jpy_str
;;

let print_jpy_to_usd jpy =
  let usd_str = string_of_float (jpy_to_usd jpy) in
  Printf.printf "%s yen are %s dollars\n" (string_of_int jpy) usd_str
;;

print_usd_to_jpy 4000.00;;
print_jpy_to_usd 100000;;
