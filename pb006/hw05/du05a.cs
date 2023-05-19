using System.Collections.Generic;
using System.Linq;
using System;

namespace pb006 {

    interface IArray<T>{

        T Get(int i);

        void Set(int i, T item);

        int Size();

    }

    class SimpleArray<T> : IArray<T> , IEquatable<IArray<T>>
    {
        private T[] data = null;

        public SimpleArray(int size){
            data = new T[size];
            data.Initialize();
        }

        public SimpleArray(T[] newData){
            data = newData;
        }

        public bool Equals(IArray<T> other)
        {

            if (other.Size() != this.Size()) {
                return false;
            }

            for (int i = 0; i < other.Size(); ++i){

                if (!other.Get(i).Equals(this.Get(i))) {
                    return false;
                }
            }

            return true;
        }

        public override bool Equals(object obj)
        {
            return obj is IArray<T> && Equals(obj as IArray<T>);
        }

        public T Get(int i)
        {
            return data[i];
        }

        public override int GetHashCode()
        {
            return base.GetHashCode();
        }

        public void Set(int i, T item)
        {
            data[i] = item;
        }

        public int Size()
        {
            return data.Count();
        }

        public override string ToString()
        {
            return base.ToString();
        }
    }

    class CharArray : SimpleArray<char>, IComparable<IArray<char>>, IEquatable<string>
    {
        public CharArray(int size) : base(size)
        {
        }

        public CharArray(char[] newData) : base(newData)
        {
        }

        public CharArray(string s) : base(s.ToCharArray())
        {
        }

        public int CompareTo(IArray<char> other)
        {
            if (this.Size() != other.Size()) {
                return this.Size() - other.Size();
            }

            for (int i = 0; i < other.Size(); ++i){

                char cur = this.Get(i);

                if (cur.CompareTo(other.Get(i)) != 0){
                    return cur.CompareTo(other.Get(i));
                }
            }

            return 0;
        }

        public int CompareTo(string other){
            return CompareTo(new CharArray(other));
        }

        public bool Equals(string other)
        {
            return Equals(new CharArray(other));
        }
    }
}
