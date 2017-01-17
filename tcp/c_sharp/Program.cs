using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NetMQ;
using NetMQ.Sockets;

namespace c_sharp
{
    class Program
    {

        /*
         *  Context wird in C# intern verwaltet. Es muss keine Instanz erstellt werden.
         *  https://github.com/zeromq/netmq/wiki/Migrating-to-v4
         */

        static void Main(string[] args)
        {
            var zmqSocket = new RequestSocket(">tcp://13.94.142.72:5555");  // Bind mit @tcp; Connect mit >tcp

            Console.WriteLine("Schreib etwas:");
            while (true)
            {
                zmqSocket.SendFrame(Console.ReadLine());
                Console.WriteLine(zmqSocket.ReceiveFrameString());
            }
           
        }
    }
}
