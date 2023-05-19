namespace pb006
{
    public enum TypeTag
    {
        Int,
        Bool,
        List,
        Function,
        Var,
    }

    public class Type
    {
        public TypeTag TypeTag;
        public Type[] TypeParams;
        public string Name;

        public Type(TypeTag typeTag, Type[]? typeParams = null, string name = "")
        {
            this.TypeTag = typeTag;
            this.TypeParams = typeParams ?? new Type[] { };
            this.Name = name;
        }

        public static Type Int()
        {
            return new Type(TypeTag.Int);
        }

        public static Type Bool()
        {
            return new Type(TypeTag.Bool);
        }

        public static Type List(Type a)
        {
            return new Type(TypeTag.List, new Type[] { a });
        }

        public static Type Function(Type a, Type b)
        {
            return new Type(TypeTag.Function, new Type[] { a, b });
        }

        public static Type Var(string name)
        {
            return new Type(TypeTag.Var, name: name);
        }

        public override string ToString()
        {
            switch (this.TypeTag)
            {
                case TypeTag.Int: return "int";
                case TypeTag.Bool: return "bool";
                case TypeTag.List: return "[" + this.TypeParams[0].ToString() + "]";
                case TypeTag.Function: return "(" + this.TypeParams[0].ToString() + " -> " + this.TypeParams[1].ToString() + ")";
                case TypeTag.Var: return this.Name;
            }

            return ""; // unreachable;
        }
    }
}