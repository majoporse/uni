namespace pb006 {
    public enum PayClass
    {
       Low,
       VeryLow,
       ExtremelyLow,
    }

    public struct Employee
    {
        public string name;
        public PayClass payClass;
        public int wage;
    }

}
