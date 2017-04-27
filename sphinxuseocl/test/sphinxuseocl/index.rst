
.. code-block:: useocl
    :linenos:

    -- This is a comment
    -- with multiple lines

    model Company

    -- classes

    class Employee
    attributes
      name : String
      salary : Integer
    end

    class Department
    attributes
      name : String
      location : String
      budget : Integer
    end

    class Project
    attributes
      name : String
      budget : Integer
    end

    -- associations

    association WorksIn between
      Employee[*]
      Department[1..*]
    end

    association WorksOn between
      Employee[*]
      Project[*]
    end

    association Controls between
      Department[1]
      Project[*]
    end

    -- OCL constraints

    constraints

    context Department
        -- the number of employees working in a department must
        -- be greater or equal to the number of projects
        -- controlled by the department
      inv MoreEmployeesThanProjects:
        self.employee->size >= self.project->size

    context Employee
        -- employees get a higher salary when they work on
        -- more projects
      inv MoreProjectsHigherSalary:
        Employee.allInstances->forAll(e1, e2 |
          e1.project->size > e2.project->size
            implies e1.salary > e2.salary)

    context Project
        -- the budget of a project must not exceed the
        -- budget of the controlling department
      inv BudgetWithinDepartmentBudget:
        self.budget <= self.department.budget

        -- employees working on a project must also work in the
        -- controlling department
      inv EmployeesInControllingDepartment:
        self.department.employee->includesAll(self.employee)




.. code-block:: useocl
    :linenos:

    model JungleExample
    -- ========================== Enumerations =====================================
    enum Season {winter, autumn, spring, summer}
    -- ========================== Classes ==========================================
    class Fruit end                    -- Classes used below
    abstract class ForestThing end     -- abstract classes cannot be instanciated
    class Animal end

    -- Class, Inheritance, Attributes, Operations, Local constraints
    class Banana < Fruit, ForestThing
    attributes
        length : Integer /* Integer, Real, Boolean, String */
        growthTime : Season
        -- Tuple, Bag, Set, OrderedSet, Sequence
        goodies : OrderedSet(Bag(Sequence(Set(TupleType(x:Integer,y:Real,z:String)))))
        -- Attribute initialisation
        remainingDays : Integer
            init: 0
        -- Derived attribute
        size : Real
            derived: self.length * self.remainingDays
        -- RESTRICTION/std: No invariants directly declared on attributes
        -- RESTRICTION/std: No cardinality supported for attributes (e.g. String[0..1])
    operations
        wakeUp(n : Integer):String       -- operation specified
            pre notTooMuch: n > 10 and n < self.length   -- precondition
            post growing: result > 'anaconda'            -- postcondition
        helloJungle() : String           -- operation with soil actions
            begin
                declare x : Banana ;
                WriteLine('hello') ;
                x := new Banana ;
                self.length := self.length + self.remainingDays*20+3 ;
                result := 'jungle' ;
                destroy x ;
            end
            post growing: self.length > self.length@pre  -- @pre(vious) value
        smash() : String                 -- operation/query defined in OCL
            = 'li'+'ons' -- derived/query operation defined as anOCL expression
    constraints
        -- invariants
        inv growthSeasons: self.growthTime <> Season::winter
    end -- end of class Banana
    -- ========================== Associations =====================================
    -- Associations, Roles, Cardinality
    association Eats between   -- 'association' or 'composition' or 'aggregation'
        Animal[*] role eater   -- could be followed by 'ordered'
        Banana[1] role food    -- cardinality can be [1..8,10,15..*]
        -- ...                 -- more roles here for n-ary associations
    end
    -- Association classes
    associationclass Dislike between
        Animal [0..1] role animal
        Banana[1..*] role bananas
    attributes                 -- operations can be declared as well
        reason : String
    end
    -- Qualified associations
    association Prefers between
        Animal [*] role animals qualifier (period:Season)
        Fruit[0..1] role candy
    end
    -- ========================== External Constraints =============================
    constraints
    context Banana                                     -- Constraints on Classes
        inv atLeastOne: Banana.allInstances()->size()>1
    context self:Banana                                -- Constraints on Attributes
        inv largeEnough: self.length > 3
    context Banana::wakeUp(n:Integer):String           -- Constraints on Operations
        -- Constraints on Operations
        pre justOk: self.length < 1000 and n > 12
        post notTiger: result <> 'tiger'


    class DateTime
    attributes
        nbOfMinutes : Integer
    operations
        day():Integer = self.nbOfMinutes div (24*60)
        hour():Integer = (self.nbOfMinutes).mod(24*60) div 60
        minute():Integer = self.nbOfMinutes.mod(60)
        setTime(day:Integer,hour:Integer,minute:Integer)
            begin
              self.nbOfMinutes := (day*24+hour)*60+minute
            end
        toString():String
            = 'Day #'+self.day().toString()
               +' '+self.hour().toString()+':'+self.minute().toString()
        minutesFrom(d:DateTime):Integer
            = self.nbOfMinutes - d.nbOfMinutes
    end

    class Environment
    attributes
        now : DateTime
    operations
        assert(message:String,condition:Boolean)
            begin
                if not condition then
                    WriteLine('AssertionError: '+message)
                end
            end
    end

.. code-block:: useocl
    :linenos:

    -- ? for queries, ! for actions, commands:  open, check, quit, info, help...
    open -q background.soil                               -- include a file
    ? Set{2,3}->including(7)                              -- OCL query
    ! b1 := new Banana ; chita := new Animal              -- object creation
    ! insert(chita,b1) into Eats                          -- link creation
    ! d := new Dislike between (chita,b1)                 -- object-link creation (class association)
    ! b1.length := 20                                     -- attribute assignment
    ? b1.smash()+' are nices'                             -- call of a query (defined in OCL)*
    ! destroy d                                           -- object/object-link destruction
    ! delete (chita,b1) from Eats                         -- link destruction
    ! Write('jungle'+(4+2).toString()) ; WriteLine('')    -- output
    -- ! r := ReadLine() ; i := ReadInteger() ;              -- input
    ! if not (b1.length=20) then WriteLine('error1') end  -- if then else
    ! for i in Sequence{1..4} do b := new Banana ; insert(chita,b) into Eats end



