# coding=utf-8

# TODO:0 create a scenario for valence/cci/pi
# TODO:0 check koquery90 with assert/query mixture at top
# TODO:0 check ? vs ?? + KOQuery03
# TODO:0 check koinv04: display of cls,

# TODO:0 locate model issues
# TODO:1 change the syntax of assert. assert name : ....
#        add name in metamodel and output
#        assert inv a: False
#        assert inv b: Failure
#        assert inv b
#        assert 2+3=5
#        assert b : 2+6=3
#
# TODO:0 bind object/evaluation model issuebox with scenario
#        otherwise there is no error reported when building objects
# TODO:0 add | text block to : (require analysis because before)
#        binding descriotion to elements is not compulsary
#        object
#        scenario
# TODO:0 add inheritance in cl metamodel
# TODO:0 add check for optional attributes in check
# TODO:1 add check for id attributes in check
# TODO:0 state begin and state end for objects
# TODO:0 test and test error display + error detection among files
# FIXME:0 display /tmp error in sex/use
#        for metamodels, since composed metamodels are
#        important (e.g. permissoion -> usecase)

# FIXME:0 strange printing for models
# TODO:0 check why empty entries are  ignored in glossary
#       see domain2.gls


# CAVEAT1: Scenario must import a class model now
#       This limitation should be removed.
#       At the moment it this is required because scenarios
#       are based on the pair use + soil
#       Look at SexSource and check how to remove dependency on '.use"
#       Looking at the case of empty scs file should help as well
#       See test kosyntax21 kosyntax22
#
# TODO:1 datatype: definition + replacement
# TODO:1 package: hierachy + tests
# TODO:1 improve text block metrics with ref and word
# TODO:1 add hierachyca metrics
# TODO:1 refactor SourceElement and SourceModelElement
#        a SourceElement should be a location within SourceModelFile
#        a SourceModelElement a pair for a mapping stored
#        in SourceModelFile. Review as well the notion of Location
# TODO:1 add tags {a,b,c=t} -> --@a --@b --@c=t
#       add parsingprepoc+parser+metamodel+printer
# TODO:1 add {id} semantics -> generation of ocl
#        constratint C.x{id} C.y{id]
#        ->  constraint inv none:C: C.allInstance->isUnique(c|Tuple{c.x,c.y})
# TODO:1 find a solution for option variants
#       currently the modelc interpreter support only general
#       options independent from models.
#       The scenario printer configuration has model option
#       but they are not used since modelc interpeter does not create
#       a ScenarioPrinterConfiguration.
#       It is necessary to find a way to change this to support
#       model specific option. Currently the SecenarioPrinter
#       add some attributs on the fly. This should be removed.
# TODO:1 add constraint composition[0..1,1]

# TODO:1 add sex parser to support composition
# (ScribesEnv)jmfavre@jmfavre-HP-ZBook-15:/D2/ScribesZone/ModelScripts/test/modelscripts/testcases/sex$ use -qv composition.use composition3.soil
# Warning: Insert has resulted in two aggregates for object `Wheel1'. Object `Wheel1' is already component of another object.
# Warning: Insert has resulted in two aggregates for object `Wheel1'. Object `Wheel1' is already component of another object.
# Warning: Insert has resulted in two aggregates for object `Wheel1'. Object `Wheel1' is already component of another object.
# checking structure...
# Error: Object `Wheel1' is shared by object `Car1' and object `Car3'.
# Multiplicity constraint violation in association `HasWheel':
#   Object `Wheel1' of class `Wheel' is connected to 3 objects of class `Car'
#   at association end `car' but the multiplicity is specified as `1'.
# checked structure in 1ms.
# checking invariants...
# checked 0 invariants in 0.000s, 0 failures.

"""
Warning: Operation call ...
This may lead to unexpected behavior.
You can change this check using the -oclAnyCollectionsChecks switch.
You can change this check using the -extendedTypeSystemChecks switch.

Expression " + StringUtil.inQuotes(this.stringRep(args, "")) +
					 " can never evaluate to more than an empty bag, " + StringUtil.NEWLINE +
					 "because the element types " + StringUtil.inQuotes(elemType1) +
					 " and " + StringUtil.inQuotes(elemType2) + " are unrelated.";
		}

			return "Expression " + StringUtil.inQuotes(this.stringRep(args, "")) +
					 " will always evaluate to false, " + StringUtil.NEWLINE +
					 "because the element type " + StringUtil.inQuotes(col.elemType()) +
					 " and the parameter type " + StringUtil.inQuotes(args[1].type()) + " are unrelated.";

*<input>:1:3: Warning: application of `oclIsKindOf' to a single value should be done with `.' instead of `->'.
*Warning: Insert has resulted in a cycle in the part-whole hierarchy. Object `y' is a direct or indirect part of `x'.
*Warning: Insert has resulted in two aggregates for object `z'. Object `z' is already component of another object.
*Warning: Object `x' cannot be a part of itself.

			return "Expression " + StringUtil.inQuotes(this.stringRep(args, "")) +
					 " will always evaluate to the same ordered set, " + StringUtil.NEWLINE +
					 "because the element type " + StringUtil.inQuotes(col.elemType()) +
					 " and the parameter type " + StringUtil.inQuotes(args[1].type()) + " are unrelated.";


?a1->selectByKind(B)
* <input>:1:4: Warning: application of `selectByKind' to a single value should be done with `.' instead of `->'.
The operation `selectByKind' is only applicable on collections.

"""
# TODO:0 Add Internal Fatal, Error, warning and move use trace to internal warning
#        Error during USE execution: Unexpected line (#85) in use trace:
#        "You can change this check using the -extendedTypeSystemChecks switch."
#       Add -extendedTypeSystemChecks:I  -oclAnyCollectionsChecks:I

"""
Warning: Operation call ...
This may lead to unexpected behavior.
You can change this check using the -oclAnyCollectionsChecks switch.
You can change this check using the -extendedTypeSystemChecks switch.

Expression " + StringUtil.inQuotes(this.stringRep(args, "")) + 
					 " can never evaluate to more than an empty bag, " + StringUtil.NEWLINE +
					 "because the element types " + StringUtil.inQuotes(elemType1) + 
					 " and " + StringUtil.inQuotes(elemType2) + " are unrelated.";
		}

			return "Expression " + StringUtil.inQuotes(this.stringRep(args, "")) + 
					 " will always evaluate to false, " + StringUtil.NEWLINE +
					 "because the element type " + StringUtil.inQuotes(col.elemType()) + 
					 " and the parameter type " + StringUtil.inQuotes(args[1].type()) + " are unrelated.";

*<input>:1:3: Warning: application of `oclIsKindOf' to a single value should be done with `.' instead of `->'.
*Warning: Insert has resulted in a cycle in the part-whole hierarchy. Object `y' is a direct or indirect part of `x'.
*Warning: Insert has resulted in two aggregates for object `z'. Object `z' is already component of another object.
*Warning: Object `x' cannot be a part of itself.

			return "Expression " + StringUtil.inQuotes(this.stringRep(args, "")) + 
					 " will always evaluate to the same ordered set, " + StringUtil.NEWLINE +
					 "because the element type " + StringUtil.inQuotes(col.elemType()) + 
					 " and the parameter type " + StringUtil.inQuotes(args[1].type()) + " are unrelated.";


?a1->selectByKind(B)
* <input>:1:4: Warning: application of `selectByKind' to a single value should be done with `.' instead of `->'.
The operation `selectByKind' is only applicable on collections.

"""

# TODO:1  relational class model checks
# - pas d'association n-n
# - pas de classes associatives
# - pas de composition avec 0..1 du coté du composite
# - pas d'aggregation
# - pas de generalisation
# - pas de classe abstraite
# #TODO: add support for diagram generation (-d ?)
# #TODO: add support for code generation/transformation
# TODO:1 support for rôle / × > addonly

# TODO:1 add @assertion in .ob .sc
# TODO:1 import between cl diagram could be very useful
# TODO:2 add syntax enumeration x ... end
#        easy for first and other lines, but must have context for "end"

# TODO:2 Installation procedure.
#       chmod +x for internal model-use
#       chmox +x for bin/*
# TODO:2 continue metametamodel
# - py.py contains element for annotation
# - metamodels/classes.py contains first examples
# - metamodels/parser.py contains first version of extractiing metamodel
# - megamodels/metametamodels contains first version of metaelements
# - modelscripts/metamodels.py start the parsing of metapackage
# TODO:2 full support for addOnly, readOnly
# TODO:2 add [0..1] constraint   not self.x->isUndefined
# TODO:3 disable x : Class where Class si not datatype
# TODO:2 datatype Date < String
#       this just replace x : Date by x : String
#       to simplify no "end" keyword
#       other datatype are in fact not really useful
#       since their creation is not easy
# TODO:3 support for taskmodel / kxml
# TODO:2 support for quality models
# TODO:3 support for abstract gui models
# TODO:2 support for timetracking
# TODO:1 what to do with unique nonUnique orderted
# TODO:2 enable 0package
# TODO:2 check permission analysis
# TODO:3 re parser
# TODO:3 is parser
# TODO:3 oc parser -> cl


#TODO: improve error management

#TODO: add options to bin/modelc.py (-p, -s, ...)
#TODO: check association/class metamodel

#TODO: check what to do with  (link)object destruction

#TODO3: check plantuml generation

#TODO: add support for @assert inv / query
#TODO: add support for 'include x.obm' in scenarios

# #TODO: plantuml, check how to get errors from generation

# megamodels
# ----------
# * parser
# * summary/metrics
#
# glossaries
# ----------
#
# * metamodel
# * parser
# * integration in other models
# * summary/metrics
#
# usecases
# --------
#
# * summary
# * error checking
# * printer
# * add management of description
# * priority, interface, etc.
# * scm coverage - scm
# * pmm/clm coverage -- pmm ucm
#
# classes
# -------
#
# * refactor associationClass
# * add package statement
# * spec for clm language ?
# * check a few things in the parser
# * check if comment handling is ok
# * add a few test to check result
# * coverage of invariant wrt class model
# * pmm/ucm coverage -- pmm ucm
#
# objects
# -------
#
# * summary/metrics
# * add description
# * add the possibility to include other obm files at the begining
#   (avoid circular dependencies)
# * clm coverage
#
# scenarios
# ---------
#
# * summary/metrics
# * generation of access model
# * add the possibility to include a obm
# * add description
# * spec for scm as own language (while based on soil)
# * implement assertions (inv + query)
# * ucm coverage
# * clm coverage
# * plm coverage
#
# permissions
# -----------
#
# * summary/metrics?
# * improve language
# * pmm/
#
# access
# ------
#
# * define objectives
# * define language
#
