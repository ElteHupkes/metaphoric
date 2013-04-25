# Rakefile for Metaphoric-static
# requires:
# maruku: gem install maruku
# compass: gem install compass
# mustache: gem install mustache

require 'maruku'
require 'mustache'

# Default task is build
task :default => "build"

desc "Clear build files."
task :clean do
	rm_rf "dist"
end

directory "dist"

def truncate(string, length = 15)
  string.size > length+5 ? [string[0,length],string[-5,5]].join("...") : string
end

# Load a list of posts
CONFIGS=[]
SOURCES=FileList['content/*.md'].select { |fn| !(fn =~ /\.draft\.md$/) }.sort!
SOURCES.each do |fn|
	m = /^content\/(\d{4}-\d\d-\d\d-\d\d-\d\d)-(.+)\.md$/.match(fn)
	if not m
		puts "WARNING: input file "+fn+" does not match blog format."
		next
	end
	
	# Read the first line for the title (http://stackoverflow.com/questions/1490138/reading-the-first-line-of-a-file-in-ruby)
	titleMatch = /#\s+(.+)/.match(File.open(fn, &:readline))

	if not titleMatch
		puts "WARNING No valid title match for file "+fn
		next
	end

	datetime = DateTime.strptime(m[1], '%Y-%m-%d-%H-%M')
	slug = m[2]
	cfg = {
		:input => fn,
		:slug => slug,
		:title => titleMatch[1],
		:truncated => truncate(titleMatch[1]),
		:datetime => datetime,
		:published => datetime.strftime('%B %-d, %Y')
	}

	CONFIGS.push(cfg)
end
CONFIGS[-1][:slug] = 'index'

l = CONFIGS.length
latestRange = -([3,l].min)..-1
latest = CONFIGS[latestRange]
latestFiles = latest.map { |cfg| cfg[:input] }

post = File.read('post.mustache');
CONFIGS.each_with_index do |cfg, index|
	deps = [cfg[:input], 'dist', 'post.mustache'].concat(latestFiles)
	if index < (l-1)
		cfg[:next] = CONFIGS[index+1]
		deps.push(cfg[:next][:input])
	end

	if index > 0
		cfg[:prev] = CONFIGS[index-1]
		deps.push(cfg[:prev][:input])
	end

	cfg[:link] = cfg[:slug]+'.html'
	cfg[:output] = 'dist/'+cfg[:link]
	cfg[:latest] = latest

	file cfg[:output] => deps do
		cfg[:content] = Maruku.new(File.read(cfg[:input])).to_html
		output = Mustache.render(post, cfg)
		File.open(cfg[:output], 'w') { |f| f.write(output) }
	end
end

directory "dist/css" => "dist" do
	sh "cp -r css dist/css"
end

directory "dist/images" do
	sh "cp -r images dist/images"
end
directory "dist/js" do
	sh "cp -r js dist/js"
end

file "dist/css/styles.css" => ["dist/css", "scss/styles.scss"] do
	sh "compass compile --relative-assets --sass-dir scss --css-dir dist/css --images-dir images scss/styles.scss"
end

DEPS = CONFIGS.map { |cfg| cfg[:output] }
desc "Build."
task :build => DEPS.concat(["dist/js", "dist/images", "dist/css/styles.css"])
