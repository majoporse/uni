using System;
using System.Diagnostics;
using pb006;
using System.Linq;

namespace pb006{

    // class program{
        // private static void Main(){
        //     SimpleArray<int> arr1 = new SimpleArray<int>(new int[] { 1, 2, 3 });
        //     IArray<int> arr2 = new SimpleArray<int>(new int[] { 1, 2, 3 });
        //     SimpleArray<char> arr3 = new SimpleArray<char>(new char[] { (char)1, (char)2, (char)3 });
            
            
        //     Debug.Assert(arr1.Equals(arr1)); // ~>* true
        //     Debug.Assert(arr1.Equals(arr2)); // ~>* true
        //     Debug.Assert(!arr1.Equals(arr3)); // ~>* false
        //     Debug.Assert(!arr1.Equals(123)); // ~>* false
            
            
        //     CharArray chArr1 = new CharArray("abcd");
        //     CharArray chArr2 = new CharArray("abcd");
        //     CharArray chArr3 = new CharArray("abce");
        //     CharArray chArr4 = new CharArray("abc");
            
            
        //     Debug.Assert(chArr1.Equals(chArr2)); // ~>* true
        //     Debug.Assert(!chArr1.Equals(chArr3)); // ~>* false
        //     Debug.Assert(!chArr1.Equals(chArr4)); // ~>* false
        //     Debug.Assert(chArr1.CompareTo(chArr2) == 0); // ~>* 0
        //     Debug.Assert(chArr1.CompareTo(chArr3) < 0); // ~>* any negative number
        //     Debug.Assert(chArr1.CompareTo(chArr4) > 0); // ~>* any positive number
        //     Debug.Assert(chArr1.Equals("abcd")); // ~>* true
        //     Debug.Assert(chArr1.CompareTo("abce") < 0);

        //     IFlags f1 = new Flags(4); // f1 ~>* 0000
        //     f1.Set(0, true); // f1 ~>* 1000
        //      Console.WriteLine(f1);
        //     f1.Set(2, true); // f1 ~>* 1010
        //      Console.WriteLine(f1);
        //     IFlags f2 = new Flags(new bool[] { true, false, false, true }); // f2 ~>* 1001
        //     f1.And(f2); // f1 ~>* 1000
        //     f1.Negate(); // f1 ~>* 0111
        //     Console.WriteLine(f1); // vytiskne "0111" (uvozovky nejsou součástí výstupu)
        //     f2.Or(f1); // f2 ~>* 1111
        //     Console.WriteLine(f2);

        // }
    // }
    interface IArray<T>{

        T Get(int i);

        void Set(int i, T item);

        int Size();

    }
    
    interface IFlags : IArray<bool>
    {
        void Negate();

        void And(IFlags i);

        void Or(IFlags i);

        byte GetFlags();
    }

    struct Flags : IFlags
    {
        private int size;
        private byte bits;

        public Flags(int i){
            size = i;
            bits = 0;
        }

        public Flags(bool[] newBits){
            byte index = 0;
            bits = 0;

            size = newBits.Count();
            foreach (bool bit in newBits)
            {
                if (bit){
                    bits |= (byte) (1<<(size - index - 1));
                }
                ++index;
            }
            
        }
        
        public void And(IFlags i)
        {
             bits &= i.GetFlags();
        }

        public bool Get(int i)
        {
            return (bits & (1<<(size - i - 1))) == 1<<(size - i - 1);
        }

        public byte GetFlags()
        {
            return bits;
        }

        public void Negate()
        {
            bits = (byte) ~bits;
        }

        public void Or(IFlags i)
        {
            bits |= i.GetFlags();
        }
        public void Set(int i, bool item)
        {
            byte mask = (byte) (1<<(size - i - 1));
            if (item){
                bits |= mask;
            } else{
                bits &= (byte) (~mask);
            }
        }

        public int Size()
        {
            return size;
        }

        public override string ToString(){
            string res = "";
            for (int i = 0; i < size; ++i){
                res += (Get(i)) ? (1) : (0);
            }
            return res;
        }
    }
}