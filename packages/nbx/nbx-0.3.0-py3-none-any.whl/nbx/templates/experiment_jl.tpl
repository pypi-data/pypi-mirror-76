module Experiment
export run, params
#########
include("pspace.jl")
import .PSpace: ParameterSpace


params = ParameterSpace([
{% for k,v in sweep_args %}	Axis("{{k}}", {{v}}),
{% endfor %}])


"""
This is an auto-generated function 
based on the jupyter notebook {{name}}
"""
function run({% for k,v in sweep_args %}{{k}}{% if not loop.last %}, {% endif %}{% endfor %}; {% for k,v in const_args %}{{k}}={{v}}{% if not loop.last %}, {% endif %}{% endfor %})

	{% for line in func_body %}{{line}}{% if not loop.last %}
	{% endif %}{% endfor %}

	println("\n**nbx**\nExperiment finished.")
end


#########
end
