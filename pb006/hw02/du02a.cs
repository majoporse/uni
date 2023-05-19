namespace pb006
{

    class Task01 
    {
        public static Employee CreateEmployee (int minimalWage, string name = "John Doe", PayClass payClass = PayClass.ExtremelyLow, int wage = 0)
        {

            if (wage < minimalWage) {
                wage = minimalWage;
            }

            Employee employee = new Employee();

            employee.name = name;
            employee.payClass = payClass;
            employee.wage = wage;

            return employee;
        }
    }

    class Task02 {
        public static void ChangeWage(ref pb006.Employee employee, int[] wages, float gross, out float new_gross)
        {
            employee.wage += wages[(int) employee.payClass];
            new_gross = employee.wage * gross;
        }
    }

    
}