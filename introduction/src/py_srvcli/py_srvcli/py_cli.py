import sys
import rclpy

from rclpy.node import Node

from example_interfaces.srv import AddTwoInts

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__("minimal_client_async")

        self.cli = self.create_client(AddTwoInts, "add_two_ints")

        while not self.cli.wait_for_service(1.0):
            self.get_logger().info("Waiting for service to respond...")

        self.req = AddTwoInts.Request()

    def send_request(self):
        self.req.a = int(sys.argv[1])
        self.req.b = int(sys.argv[2])

        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    minimal_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(minimal_client)

        if minimal_client.future.done():
            try:
                response = minimal_client.future.result()
            except Exception as e:
                message = f"Result raised an exception: {e}"
            else:
                a = minimal_client.req.a
                b = minimal_client.req.b
                summation = response.sum

                message = f"Result of add_two_ints: {a} + {b} = {summation}"
            finally:
                minimal_client.get_logger().info(message)
            
            break
    
    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()