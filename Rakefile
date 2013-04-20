# Rakefile for Metaphoric-static
# requires json: gem install json
require 'json'

# Default task is build
task :default => "build"


desc "Clear build files."
task :clean do
	rm_rf "build"
end

directory "build"

# Load post configurations
SRC=FileList['content/*.json']
SOURCES=[]
DEPS=[]
SRC.each do |fn|
	cfg = JSON.parse(File.read(fn))
	if cfg.has_key?("draft") and cfg["draft"]
		next
	end

	cfg['basename'] = fn.gsub(/content\/(.+)\.json/, '\1')

	if not cfg.has_key?("source")
		md = "content/"+cfg['basename']+".md"
		html = "content/"+cfg['basename']+".html"
		if File.exists?(md)
			cfg['source'] = md
		elsif File.exists?(html)
			cfg['source'] = html
		else
			next
		end
	end

	# Create a string slug (http://stackoverflow.com/questions/4308377/ruby-post-title-to-slug)
	cfg['slug'] = cfg['title'].downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
	outputfile = 'content/'+cfg['slug']+'.html'
	cfg['filename'] = fn

	SOURCES.push(cfg)
	DEPS.push(outputfile)

	file outputfile => [fn] do
		puts "Generate "+outputfile
	end
end
SOURCES.sort_by { |hsh| hsh[:zip] }

file "build/index.html" => DEPS do
	puts "Generate index!"
end

desc "Build."
task :build => ["build/index.html"] do

end