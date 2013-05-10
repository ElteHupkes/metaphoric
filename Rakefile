# Rakefile for Metaphoric-static
# requires:
# kramdown: gem install kramdown
# compass: gem install compass
# mustache: gem install mustache
# coderay: gem install coderay

require 'kramdown'
require 'mustache'

# Default task is build
task :default => "build"

desc "Clear build files."
task :clean do
	rm_rf "dist"
end

directory "dist"

def truncate(string, length = 20)
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

l = CONFIGS.length
latestRange = -([5,l].min)..-1
latest = CONFIGS[latestRange].reverse
latestFiles = latest.map { |cfg| cfg[:input] }

layout = File.read('layout.mustache')
post = File.read('post.mustache')

mdOptions = {
	:coderay_line_numbers => :table
}

CONFIGS.each_with_index do |cfg, index|
	deps = [cfg[:input], 'dist', 'post.mustache', 'layout.mustache'] + latestFiles
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
		puts "Generating post "+cfg[:title]
		cfg[:content] = Kramdown::Document.new(File.read(cfg[:input]), mdOptions).to_html
		cur = Mustache.render(post, cfg)
		cfg[:content] = cur
		output = Mustache.render(layout, cfg)
		File.open(cfg[:output], 'w') { |f| f.write(output) }
	end
end

DEPS = CONFIGS.map { |cfg| cfg[:output] }
file "dist/index.html" => DEPS do
	sh "cp "+DEPS[-1]+" dist/index.html"
end

file "dist/all-posts.html" => DEPS + ["all_posts.mustache", 'layout.mustache'] do
	puts "Generating post list.."
	tmpl = File.read('all_posts.mustache')
	page = Mustache.render(tmpl, :posts => CONFIGS.reverse)
	output = Mustache.render(layout, :content => page, 
		:title => "All posts", :link => "/all-posts.html")
	File.open("dist/all-posts.html", 'w') { |f| f.write(output) }
end

file "dist/favicon.ico" => ["favicon.ico", "dist"] do
	sh "cp favicon.ico dist/favicon.ico"
end

task :static => ["dist"] do
	sh "cp -r js dist/js"
	sh "cp -r images dist/images"
	sh "cp -r css dist/css"
	sh "cp favicon.ico dist/favicon.ico"
end

file "dist/css/styles.css" => [:static, "scss/styles.scss"] do
	sh "compass compile --relative-assets --sass-dir scss --css-dir dist/css --images-dir images scss/styles.scss"
end

task :compile => ["dist/index.html", "dist/all-posts.html", "dist/css/styles.css"]

desc "Build."
task :build => [:static, :compile]

task :create, :title do |t, args|
	t = DateTime.now
	part = t.strftime('%Y-%m-%d-%H-%M')
	filename = args[:title].downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
	filename = part+'-'+filename+'.md'
	puts "Creating content/"+filename+"..."

	File.open("content/"+filename, 'w') { |f| f.write('# '+args[:title]) }
end

task :release do
	sh "ssh elte@hupkes.org bash --login -c './metaphoric-release.sh'"
end

