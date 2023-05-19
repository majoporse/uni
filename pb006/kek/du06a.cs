using System;
using System.Runtime.Serialization;
using System.Diagnostics;

class lol{
    public void foo(){
        Console.Write("kokot");
    }
}

namespace pb006{

    interface IA {
     void PrintIt(string s);
    }
    interface IB {
        void PrintIt(string s);
    }
    class MyClass : IA, IB {
        class asd{

        }
    void IA.PrintIt(string s) {
        Console.WriteLine(s);
    }
    void IB.PrintIt(string s) {
        Console.WriteLine(s);
    }

    public void PrintIt(string s) {
        Console.WriteLine(s);
    }
}

    class program{
        static void Main(){

            global ::lol a = new global :: lol();
            a.foo();

            MyClass c = new MyClass();
            c.PrintIt("MyClass");
            IA ai = (IA) c;
            ai.PrintIt("IA");
            (c as IB).PrintIt("IB");
            string? s = default;
            // string a = s!;

            // CheckingRingBuffer<int> b = new CheckingRingBuffer<int>(1);
            // b.Push(1);
            // // b.Push(2); // způsobí vyhození výjimky RingBufferFullException
            // Debug.Assert(b.Pop() == 1); // ~>* 1
            // // b.Pop();

            // IQueueTools<int>.ForcePush(b, 3);
            // IQueueTools<int>.ForcePush(b, 4);
            // Debug.Assert(b.Pop() == 4); // ~>* 4

            // IQueueTools<int>.WeakPush(b, 3);
            // IQueueTools<int>.WeakPush(b, 4);
            // Debug.Assert(b.Pop() == 3); // ~>* 3

            // b.Push(5);
            // Debug.Assert(IQueueTools<int>.SafePop(b, 6) == 5); // ~>* 5
            // Debug.Assert(IQueueTools<int>.SafePop(b, 6) == 6); // ~>* 6

        }
    }
    public class RingBufferException : Exception
    {
        public RingBufferException()
        {
        }

        public RingBufferException(string message) : base(message)
        {
        }

        public RingBufferException(string message, Exception innerException) : base(message, innerException)
        {
        }

    }

    public class RingBufferFullException : RingBufferException
    {
        public RingBufferFullException()
        {
        }

        public RingBufferFullException(string message) : base(message)
        {
        }

        public RingBufferFullException(string message, Exception innerException) : base(message, innerException)
        {
        }

    }

    public class RingBufferEmptyException : RingBufferException
    {
        public RingBufferEmptyException()
        {
        }

        public RingBufferEmptyException(string message) : base(message)
        {
        }

        public RingBufferEmptyException(string message, Exception innerException) : base(message, innerException)
        {
        }

    }

    class CheckingRingBuffer<T> : RingBuffer<T>{
    
        public CheckingRingBuffer(int count) : base(count)
        {
        }

        public CheckingRingBuffer(T[] buffer) : base(buffer)
        {
        }

        public override void Push(T val){
            if (this.count == this.buffer.Length){
                throw new RingBufferFullException($"Push failed on {val}");
            }
            base.Push(val);
        }

        public override T Pop(){
            if (this.count == 0){
                throw new RingBufferEmptyException($"Pop failed");
            }
            return base.Pop();
        }

    }

    static class IQueueTools<T>{

        public static void ForcePush(IQueue<T> q, T val){
            try {
                q.Push(val);
            }
            catch(RingBufferFullException){
                try{
                    q.Pop();
                    q.Push(val);
                }
                catch(RingBufferEmptyException e2){
                    throw new RingBufferFullException($"ForcePush failed on {val}", e2);
                }
            }

        }

        public static void WeakPush(IQueue<T> q, T val){
            try{
                q.Push(val);
            }
            catch(RingBufferFullException){}
        }

        public static T SafePop(IQueue<T> q, T def){
            try{
                return q.Pop();
            }
            catch(RingBufferEmptyException e){
                return def;
            }
        }
    }
}