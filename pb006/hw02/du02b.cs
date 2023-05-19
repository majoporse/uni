using  System.Collections.Generic;

namespace pb006
{

    class Task03 
    {
        public static IEnumerable<Node> ChildrenByCost(Node[] nodes, int[] costs){
            
            Node[] res = (Node[]) nodes.Clone();
            int[] cos = (int[]) costs.Clone();
            System.Array.Sort(cos, res);
            for (int i = 0; i < res.Length; ++i){
                yield return res[i];
            }
        }

        public static IEnumerable<int> ByCost(Node node){
            Queue<Node> q = new Queue<Node> {};
            q.Enqueue(node);
            while (q.Count != 0){

                Node current = q.Dequeue();

                yield return current.value;

                if (current.costs == null){
                    continue;
                }

                foreach (Node n in ChildrenByCost(current.children, current.costs))
                {
                    q.Enqueue(n);
                }
                
            }
        }
    }
    class program{
        public static void Main(string[] args)
        {   // Testing
            Node root = new Node();
            root.value = 10;
            root.costs = new int[] { 22, 30, 21 };

            Node node1 = new Node();
            node1.value = 3;
            node1.costs = new int[] { 25, 6, 5 };

            Node node2 = new Node();
            node2.value = 8;
            node2.costs = new int[] { 8, 10 };

            Node node3 = new Node();
            node3.value = 5;
            node3.costs = new int[] { 10, 18, 13 };

            Node node4 = new Node();
            node4.value = 1;

            Node node5 = new Node();
            node5.value = 11;

            Node node6 = new Node();
            node6.value = 4;

            Node node7 = new Node();
            node7.value = 9;

            Node node8 = new Node();
            node8.value = 12;

            Node node9 = new Node();
            node9.value = 2;

            Node node10 = new Node();
            node10.value = 7;

            Node node11 = new Node();
            node11.value = 6;

            node1.children = new Node[] { node4, node5, node6 };
            node2.children = new Node[] { node7, node8 };
            node3.children = new Node[] { node9, node10, node11 };
            root.children = new Node[] { node1, node2, node3 };

            foreach (int i in Task03.ByCost(root))
            {
                System.Console.WriteLine(i);
            }
}

    }
}