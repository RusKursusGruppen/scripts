structure Skema =
struct
open List;

(* Utility functions. *)
fun id x = x
fun const x _ = x
fun flip f x y = f y x

fun updateWith (key, value) [] _ = [(key, value)]
  | updateWith (key, value) ((key', value')::ls) f =
    if key = key'
    then (key, f value' value)::ls
    else (key', value')::updateWith (key, value) ls f

fun update (key, value) l = updateWith (key, value) l (flip const)

fun curry f x y = f (x,y)

fun uncurry f (x, y) = f x y

(* Data type definitions. *)
type rus = string

type team = string * rus list
fun name (n, _)  = n
fun russ (_, rs) = rs

type task = string

type activity = int * string
fun day (d, _) = d
fun job (_, j) = j

type schedule = (activity * team option) list
fun activity (a, _) = a
fun team     (_, t) = t

(* Domain-specific helper functions. *)
local
    fun blank' activity = (activity, NONE)
in fun blankSchedule l = map blank' l end

fun byActivity act = filter (fn s => job (activity s) = job act)
fun byTeam tm    = filter (fn s => team s = SOME tm)

fun orderTeams sch = (* Ordered by busyness. *)
    let fun cmp (team1, team2) =
            Int.compare (length (byTeam team1 sch),
                         length (byTeam team2 sch))
    in Listsort.sort cmp end

fun orderActivities sch team = (* Order based on whether the team has done this before. *)
    let fun cmp (act1, act2) =
            Int.compare (length (byActivity act1 (byTeam team sch)),
                         length (byActivity act2 (byTeam team sch)))
    in Listsort.sort cmp end

fun acceptable team sch rules act =
    let fun check rule = rule team act sch
    in all check rules end

local
    fun available (activity, NONE) = true
      | available (activity, _)    = false
in
fun unassigned l = map activity (filter available l)
end

(* Actual schedulizer. *)
fun schedulize activities teams rules =
    let fun candidates sch team uns =
            orderActivities sch team (filter (acceptable team sch rules) uns)
        fun schedulize' sch =
            case orderTeams sch teams of
                [] => raise Fail "No teams"
              | ts => tryAssign sch (unassigned sch) ts
        and tryAssign _ _ [] = raise Fail "Cannot solve with given constraints"
          | tryAssign sch [] _ = sch
          | tryAssign sch uns (t::ts) =
            case candidates sch t uns of
                []       => tryAssign sch uns ts
              | (act::_) => schedulize' (update (act, SOME t) sch)
    in schedulize' (blankSchedule activities) end

(* Input and parsing functions. *)
local
    fun chomp' []      = []
      | chomp' (c::cs)  = if (Char.isSpace c) then chomp' cs else (c::cs)
    val chomp = implode o rev o chomp' o rev o chomp' o explode
    val lines = String.tokens (fn c => c = #"\n")
    fun readLines file =
        let val infile = TextIO.openIn file
        in map chomp (lines (TextIO.inputAll infile))
           before TextIO.closeIn infile end
    fun processActivities ((d, t)::rest) p i =
        let val i' = if p = d then i else i+1
        in case processActivities rest d i' of
               (d'::ds, (p, t')::rest') =>
               if d' <> d then (d::d'::ds, (i', t)::(p, t')::rest')
               else (d'::ds, (i', t)::(p, t')::rest')
             | _ => ([d], [(i', t)])
        end
      | processActivities [] _ _ = ([], [])
    fun error s i = raise Fail ("Parse error in file " ^ s ^ " at line " ^ Int.toString i)
in
fun readFile file parser =
    let val lines   = readLines file
        val linenos = tabulate (length(lines), curry op+ 1)
    in map parser (ListPair.zip (lines, linenos)) end
fun readActivities file =
    let fun parse (line, i) =
            case String.tokens (curry op= #":") line of
                [d, t] => (chomp d, chomp t)
              | _      => error file i
    in processActivities (readFile file parse) "" ~1 end
fun readTeams file =
    let fun parse (line, i) =
            case String.tokens (fn c => c = #":") line of
                [d, t] => (chomp d, map chomp (String.fields (curry op= #",") t))
              | _      => error file i
    in readFile file parse end
end

(* Rules and constraints. *)
local
    fun schedPos act (s :: ss) i =
        if act = activity s then i else schedPos act ss (i+1)
      | schedPos act [] i = i (* Should never happen. *)
in
fun minPause x team act sch =
    let val pos = schedPos act sch 0
        fun checkDist act' = abs (schedPos act' sch 0 - pos) > x
    in (all checkDist o map activity o byTeam team) sch end
fun noRepeat team act sch =
    let fun checkDist act' = abs (day act' - day act) > 1
    in (all checkDist o map activity o byActivity act o byTeam team) sch end
end

(* Prettyprinting schedule. *)
local
    fun f (s, l) = updateWith (day (activity s), [(job (activity s), valOf (team s))]) l (curry op@)
    val byDay = foldl f []
    fun commasize [] = ""
      | commasize [x] = x
      | commasize (x::xs) = x ^ ", " ^ commasize xs
    fun describeAssignment (job, team:team) =
        "\\item[" ^ job ^ "]: " ^ name team ^ " (" ^ commasize (russ team) ^ ")\n"
    fun describe' days (day, asgns) = "\\textbf{" ^ nth (days, day) ^ "}\n"
                                      ^ "\\begin{description}\n"
                                      ^ String.concat (map describeAssignment asgns)
                                      ^ "\\end{description}\n"
in
fun describe days = String.concat o map (describe' days) o byDay
end

(* Final interface. *)
fun schedulizeFromFiles activityfile teamfile =
    let val rules = [minPause 2, noRepeat]
        val (days, activities) = readActivities activityfile
        val teams              = readTeams teamfile
    in (days, schedulize activities teams rules) end

fun laySchedule activityfile teamfile =
    let val (days, schedule) =
            schedulizeFromFiles activityfile teamfile
    in print (describe days schedule) end

local
    fun getarg arg (param::data::rest) =
        if param = ("--"^arg) then data else getarg arg (data::rest)
      | getarg arg _ = raise Fail ("No --" ^ arg ^ " argument found")

    fun main args = laySchedule (getarg "activityfile" args) (getarg "teamsfile" args)
in
val _ = main (CommandLine.arguments ())
end

end
