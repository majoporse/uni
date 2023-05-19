using System.Diagnostics;
using System;

namespace pb006
{
    class Node<K, V>
    {
        public K Key;
        public V Value;
        public Node<K, V> Lt;
        public Node<K, V> Rt;

        public Node(K key, V value)
        {
            Key = key;
            Value = value;
        }
    }

    class BinTree<K, V> where K : System.IComparable<K>
    {
        private Node<K, V> Root;

        public BinTree(Node<K, V> root = null)
        {
            Root = root;
        }

        private static int SizeFrom(Node<K, V> node)
        {
            if (node == null)
                return 0;

            return 1 + SizeFrom(node.Lt) + SizeFrom(node.Rt);
        }

        public int Size()
        {
            return SizeFrom(Root);
        }

        private static int HeightFrom(Node<K, V> node)
        {
            if (node == null)
                return 0;

            return 1 + Math.Max(HeightFrom(node.Lt), HeightFrom(node.Rt));
        }

        public int Height()
        {
            return HeightFrom(Root);
        }

        private static V LookupFrom(Node<K, V> node, K key)
        {
            if (node == null)
                return default(V);

            if (key.CompareTo(node.Key) == 0)
                return node.Value;

            if (key.CompareTo(node.Key) < 0)
                return LookupFrom(node.Lt, key);

            return LookupFrom(node.Rt, key);
        }

        public V Lookup(K key)
        {
            return LookupFrom(Root, key);
        }

        private static void InsertTo(Node<K, V> node, Node<K, V> newNode)
        {
            Debug.Assert(node != null);

            if (newNode.Key.CompareTo(node.Key) == 0)
            {
                node.Value = newNode.Value;
            }

            else if (newNode.Key.CompareTo(node.Key) < 0)
            {
                if (node.Lt == null)
                {
                    node.Lt = newNode;
                }
                else
                {
                    InsertTo(node.Lt, newNode);
                }
            }

            else
            {
                if (node.Rt == null)
                {
                    node.Rt = newNode;
                }
                else
                {
                    InsertTo(node.Rt, newNode);
                }
            }
        }

        public void Insert(K key, V value)
        {
            Node<K, V> newNode = new Node<K, V>(key, value);

            if (Root == null)
                Root = newNode;
            else
                InsertTo(Root, newNode);
        }

        private static string ToStringFrom(Node<K, V> node)
        {
            Debug.Assert(node != null);

            return String.Format("(k={0}, v=\"{1}\"{2}{3})",
                node.Key,
                node.Value,
                (node.Lt == null ? "" : ", lt=" + ToStringFrom(node.Lt)),
                (node.Rt == null ? "" : ", rt=" + ToStringFrom(node.Rt))
            );
        }

        public override string ToString()
        {
            return Root == null ? "empty" : String.Format("root={0}", ToStringFrom(Root));
        }
    }
}