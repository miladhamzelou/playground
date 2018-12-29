


require "hiredis"
require "hiredis/reader"
require "test/unit"

class TestHiredis < Test::Unit::TestCase

  def test_1
    conn = Hiredis::Connection.new
    conn.connect("127.0.0.1", 6379)
    conn.write ["DEL", "speed", "awesome"]
    conn.read

    conn.write ["SET", "speed", "awesome"]
    assert_equal(conn.read, "OK")

    puts conn.write ["GET", "speed"]
    assert_equal(conn.read, "awesome")

    reader = Hiredis::Reader.new
    reader.feed("*2\r\n$7\r\nawesome\r\n$5\r\narray\r\n")
    assert_equal(reader.gets, ["awesome", "array"])
  end
end
