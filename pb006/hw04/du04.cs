using System.Collections.Generic;
using System;
using KVPair = System.Collections.Generic.KeyValuePair<int, string>;
using System.Diagnostics;

namespace pb006{
    
    // class program{
    //     public static void Main(){
            
            // KeyValuePair<int, string> a = new KeyValuePair<int, string>(1, "a");
            // List<KeyValuePair<int, string>> lol = new List<KeyValuePair<int, string>>();
            // lol.Add(a);
            // OrderedListMap kek = new OrderedListMap(lol);
            // // kek.Insert(3, "3");
            // // kek.Insert(2, "aksjdfhb");
            // // foreach(KeyValuePair<int, string> cur in lol){
            // //     Console.WriteLine("{0}", cur.ToString());
            // // }
            // KVPair[] init = new KVPair[] { new KVPair(1, "a"), new KVPair(5, "e"), new KVPair(3, "c") };
            
            // ListMap listM = new ListMap(init);
            // Debug.Assert(listM.GetValue(1) == "a");
            // Debug.Assert(listM.GetValue(2) == null);
            // listM.Insert(2, "b");
            // // Console.WriteLine(listM.GetData().ToString()); // [(1, "a"), (5, "e"), (3, "c"), (2, "b")];
            // Debug.Assert(listM.IsListBased() == true);
            // // listM.GetRank(3); // chyba kompilace, ListMap nedefinuje GetRank

            // OrderedListMap orderedListM = new OrderedListMap(init);
            // Debug.Assert(orderedListM.GetValue(1) == "a");
            // Debug.Assert(orderedListM.GetValue(2) == null);
            // orderedListM.Insert(2, "b");
            // List<KVPair> aaa = orderedListM.GetData();
            // // Console.WriteLine("{0}", aaa.ToString()); //== [(1, "a"), (2, "b"), (3, "c"), (5, "e")]);
            // Debug.Assert(orderedListM.IsListBased() == true);
            // Debug.Assert(orderedListM.GetRank(3) == 2);
            // Console.WriteLine(orderedListM.GetRank(1));

            // BinTreeMap binTreeM = new BinTreeMap(init);
            // Debug.Assert(binTreeM.GetValue(1) == "a");
            // Debug.Assert(binTreeM.GetValue(2) == null);
            // binTreeM.Insert(2, "b");
            // // binTreeM.GetData(); // ~>* root=(k=1, v="a", rt=(k=5, v="e", lt=(k=3, v="c", lt=(k=2, v="b
            // Debug.Assert(binTreeM.IsListBased() == false); // ~>* false
            // Debug.Assert(binTreeM.Height() ==  4);

            // BaseMap baseM = listM;
            // Debug.Assert(baseM.GetValue(1) == "a");
            // Debug.Assert(baseM.GetValue(4) == null);
            // baseM.Insert(4, "d");
            // // baseM.GetData(); // chyba kompilace, BaseMap nedefinuje GetData
            // listM.GetData(); // [(1, "a"), (5, "e"), (3, "c"), (2, "b"), (4, "d")]
            // Debug.Assert(baseM.IsListBased() == null);

            // ListMap oListMap = orderedListM;
            // Debug.Assert(oListMap.GetValue(1) == "a");
            // Debug.Assert(oListMap.GetValue(4) == null);
            // oListMap.Insert(4, "d");
            // oListMap.GetData(); // ~>* [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")]
            // Debug.Assert(oListMap.IsListBased() == true);

    //     }
    // }


    abstract class BaseMap
    {
        public abstract string GetValue(int Key);
        public abstract void Insert(int Key, string Val);
        public abstract int Size();
        public bool? IsListBased(){
            return null;
        }
        public bool IsEmpty(){
            return this.Size() == 0;
        }
    }


    class ListMap : BaseMap
    {
        protected List<KeyValuePair<int, string>> data = new List<KVPair>();
        
        public ListMap(IEnumerable<KeyValuePair<int, string>> NewData){
            foreach(KVPair n in NewData){
                data.Add(n);
            }
        }

        public override string GetValue(int Key){
            foreach (KeyValuePair<int, string> cur in data){
                if (cur.Key == Key){
                    return cur.Value;
                }
            }
            return null;
        }

        public override void Insert(int Key, string Val){
            data.Add(new KeyValuePair<int, string>(Key, Val));
        }

        public new bool? IsListBased(){
            return true;
        }

        public List<KeyValuePair<int, string>> GetData(){
            return data;
        }
        public override int Size(){
            return data.Count;
        }

    }


    class OrderedListMap: ListMap
    {
        private IComparer<KeyValuePair<int, string>> comparer = Comparer<KeyValuePair<int, string>>.Create((a, b) => a.Key - b.Key);

        // private List<KeyValuePair<int, string>> data;

        public OrderedListMap(IEnumerable<KeyValuePair<int, string>> newData) :base(newData){
            data.Sort(comparer);
        }

        public override string GetValue(int key){
            int index = data.BinarySearch(new KeyValuePair<int, string>(key, ""), comparer);
            return (index < 0) ? (null) : (data[index].Value);
        }

        public override void Insert(int Key, string Val){
            KeyValuePair<int, string> newItem = new KeyValuePair<int, string>(Key, Val);
            int index = data.BinarySearch(newItem, comparer);
            // Console.WriteLine("{0}", index);
            data.Insert(~index, newItem);
        }

        public int GetRank(int key){
            int index = data.BinarySearch(new KeyValuePair<int, string>(key, ""), comparer);
            return (index >= 0) ? (index) : (-1);
        }


    }

    class BinTreeMap : BaseMap
    {
        private BinTree<int, string> tree;

        public BinTreeMap(IEnumerable<KeyValuePair<int, string>> newTree){

            tree = new BinTree<int, string>(null);

            foreach(KeyValuePair<int, string> a in newTree){
                tree.Insert(a.Key, a.Value);
            }
        }

        public override string GetValue(int key){
            return tree.Lookup(key);
        }

        public override void Insert(int key , string val){
            tree.Insert(key, val);
        }

        public new bool? IsListBased(){
            return false;
        }

        public BinTree<int, string> GetData(){
            return tree;
        }

        public int Height(){
            return tree.Height();
        }

        public override int Size(){
            return tree.Size();
        }
    }
}