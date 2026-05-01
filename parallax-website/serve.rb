require 'socket'

ROOT = File.expand_path(File.dirname(__FILE__))
PORT = 8000

MIME = {
  '.html' => 'text/html',
  '.css'  => 'text/css',
  '.js'   => 'application/javascript',
  '.json' => 'application/json',
  '.png'  => 'image/png',
  '.jpg'  => 'image/jpeg',
  '.svg'  => 'image/svg+xml',
  '.ico'  => 'image/x-icon',
}

server = TCPServer.new('0.0.0.0', PORT)
$stderr.puts "Serving #{ROOT} on http://localhost:#{PORT}"

loop do
  client = server.accept
  request = client.gets
  next client.close unless request

  path = request.split(' ')[1]
  path = '/index.html' if path == '/'
  filepath = File.join(ROOT, path)

  if File.exist?(filepath) && !File.directory?(filepath)
    ext = File.extname(filepath)
    mime = MIME[ext] || 'application/octet-stream'
    body = File.binread(filepath)
    client.print "HTTP/1.1 200 OK\r\nContent-Type: #{mime}\r\nContent-Length: #{body.bytesize}\r\nConnection: close\r\n\r\n"
    client.print body
  else
    client.print "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n404 Not Found"
  end
  client.close
end
