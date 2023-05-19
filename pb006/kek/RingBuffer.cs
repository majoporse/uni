using System;

namespace pb006
{
    public interface IQueue<T>
    {
        void Push(T val);
        T Pop();
    }

    public class RingBuffer<T> : IQueue<T>
    {
        protected T[] buffer;
        private int first;
        protected int count;

        public RingBuffer(int count)
        {
            this.buffer = new T[count];
            this.first = 0;
            this.count = 0;
        }

        public RingBuffer(T[] buffer)
        {
            this.buffer = buffer;
            this.first = 0;
            this.count = 0;
        }

        public virtual void Push(T val)
        {
            this.buffer[(this.first + this.count) % this.buffer.Length] = val;
            this.count += 1;
        }

        public virtual T Pop()
        {
            T result = this.buffer[this.first];
            this.first = (this.first + 1) % this.buffer.Length;
            this.count -= 1;
            return result;
        }
    }
}
