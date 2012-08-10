structure Hold =
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

val sum = foldl op+ 0

fun avg xs = sum xs div length xs

(* Data type definitions. *)
datatype gender = M | F
type rus = string * gender * int
fun rusname (n, _, _)   = n
fun rusage  (_, _, a)   = a
fun rusgender (_, g, _) = g

type team = string * rus list
fun name (n, _)  = n
fun russ (_, rs) = rs

(* Domain specific helper functions. *)
val avgAge = avg o map rusage o russ

val femaleCount = length o filter (curry op= F o rusgender) o russ

fun swap teams rus1 rus2 =
    let fun swap'' r = if r = rus1 then rus2
                       else if r = rus2 then rus1
                       else r
        fun swap' team = (name team, map swap'' (russ team))
    in map swap' teams end

fun forRuss f teams =
    let fun forRuss' team = map f (russ team)
    in concat (map forRuss' teams) end

(* Input and parsing functions. *)
local
    fun chomp' []      = []
      | chomp' (c::cs) = if (Char.isSpace c) then chomp' cs else (c::cs)
    val chomp = implode o rev o chomp' o rev o chomp' o explode
    val lines = String.tokens (fn c => c = #"\n")
    fun readLines file =
        let val infile = TextIO.openIn file
        in map chomp (lines (TextIO.inputAll infile))
           before TextIO.closeIn infile end
    fun error s i = raise Fail ("Parse error in file " ^ s ^ " at line " ^ Int.toString i)
in
val readTeamNames = readLines
fun readRuss file =
    let val lines   = readLines file
        val linenos = tabulate (length(lines), curry op+ 1)
        fun parseGender "M" _ = M
          | parseGender "F" _ = F
          | parseGender _   i = error file i
        fun parseAge s i = case Int.fromString s of
                               SOME x => x
                             | NONE   => error file i
        fun parser (line, i) =
            case String.fields (curry op= #",") line of
                [name, gender, age] => (name,
                                        parseGender (chomp gender) i,
                                        parseAge (chomp age) i)
              | _                   => error file i
    in map parser (ListPair.zip (lines, linenos)) end
end

fun initialAssign teams rs' =
    let fun assign _ [] res = res
          | assign [] rs res = assign teams rs res
          | assign (t::ts) (r::rs) res =
            let val res' = updateWith (name t, [r]) res (curry op@)
            in assign ts rs res' end
        val result = assign teams rs' teams
        val check = all (fn team => length (russ team) > 0)
    in if not (check result)
       then raise Fail "Cannot assign at least one person to every team"
       else result end

local
    fun judgeAge teams =
        let val avgs   = map avgAge teams
            val avravr = avg avgs
            val agedev = sum (map (abs o curry op- avravr) avgs)
        in 0-agedev end

    fun judgeGender teams =
        let val counts = map femaleCount teams
            val femavg = avg counts
            fun judge team = if femaleCount team > femavg+1
                             then ~100 else 0
        in sum (map judge teams) end

    fun quality teams =
        judgeAge teams + judgeGender teams

    fun assignQualities frobs =
        ListPair.zip (map quality frobs, frobs)

    fun pickBest (f::frobs) =
        let fun pick ((q', t'), (q, t)) =
                if (q' > q) then (q', t') else (q, t)
        in foldl pick f frobs end
      | pickBest _ = raise Fail "No teams?"

    fun frobTeams teams =
        let fun mkSwaps rus1 = (forRuss (swap teams rus1) teams)
        in concat (forRuss mkSwaps teams) end

    fun optimize' q teams =
        let val (q', teams') = pickBest (assignQualities (frobTeams teams))
        in if q' > q
           then optimize' q' teams'
           else teams
        end
in
fun optimize teams = optimize' (quality teams) teams
end

fun assignTeams rusfile teamsfile =
    let fun mkTeam teamname = (teamname, [])
        val teams = map mkTeam (readTeamNames teamsfile)
        val russ  = readRuss rusfile
        val initial = initialAssign teams russ
    in optimize initial end

local
    fun commasize [] = ""
      | commasize [x] = x
      | commasize (x::xs) = x ^ ", " ^ commasize xs
    fun teamStr team = name team ^ ": " ^ commasize (map rusname (russ team))
    fun printTeam team = print (teamStr team ^ "\n")
in
fun printTeams teams = (map printTeam teams; ())
end

local
    fun getarg arg (param::data::rest) =
        if param = ("--"^arg) then data else getarg arg (data::rest)
      | getarg arg _ = raise Fail ("No --" ^ arg ^ " argument found")

    fun main args = printTeams (assignTeams (getarg "rusfile" args) (getarg "teamnamesfile" args))
in
val _ = main (CommandLine.arguments ())
end

end
