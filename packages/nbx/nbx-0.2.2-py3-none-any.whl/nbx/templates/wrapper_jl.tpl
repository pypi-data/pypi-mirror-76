using ArgParse
include("./pspace.jl")
include("./experiment.jl")
import .PSpace: get_param
import .Experiment: run, params


settings = ArgParseSettings()
@add_arg_table! settings begin
    "--job-id"
        help = "Job-id provided by job manager"
    "--task-id"
        help = "Task-id provided by job manager"
    "--results-dir"
        help = "Directory where results are stored"
end

parsed_args = parse_args(ARGS, settings)
println("Parsed args:")
for (arg,val) in parsed_args
    println("  $arg  =>  $val")
end


t  = parse(Int, parsed_args["task-id"])
rd = joinpath(parsed_args["results-dir"],"$t")

xargs = get_param(params, t)
if !isdir(rd) mkdir(rd) end
run(xargs...; task_id=t, results_dir=rd)




