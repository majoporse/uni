using System;

namespace pb006
{
    class Program
    {
        public static int Main()
        {

            return 0;
        }
    }

    class Task01
    {
        public static int SumDivisors(int n){
            int res = 0;
            for (int i = 1; i <= Math.Sqrt(n); ++i){
                if (n % i == 0){
                    if ( i == n ){
                        continue;
                    }
                    if (n / i == i || n / i == n){
                        res += i;
                    } else {
                        res += i + n / i;
                    }
                }
            }
            return res;
        }
    }

    class Task02
    {
        public static string Silence(string str, char[] array){
            string res = str;
            for (int i = 0; i < res.Length; ++i){
                
                foreach(char c in array){

                    if (res[i] == c) {
                        res = res.Remove(i,1);
                        --i;
                        break;
                    }
                }
            }
            return res;
        }
    }
    class Task03
    {
        public static string Unpack(string str){
            string rest = str;
            string result = "";
            while (rest.Length > 0){ 
                
                int first = rest.IndexOf('(');
                
                if (first == -1){
                    result += rest;
                    break;
                }

                result += rest.Substring(0, first);
                int sec = rest.IndexOf(')');
                //parse

                string s = rest.Substring(first + 1, sec - first - 1);
                string[] strings = s.Split(',');

                int iter = Int32.Parse(strings[0]);

                for (int i = 0; i < iter; ++i) {
                    result += strings[1];
                }

                //end of parsing
                if (sec + 1 == rest.Length){
                    break;
                }

                rest = rest.Substring(sec + 1 );
                
            }
            return result;
        }
    }
}