# Rakefile for Metaphoric-static
# requires json: gem install json
require 'json'

# Default task is build
task :default => "build"

desc "Clear build files."
task :clean do
	rm_rf "dist"
end

directory "dist"

# Load post configurations
SRC=FileList['content/*.json']
SOURCES=[]
DEPS=[]
SRC.each do |fn|
	cfg = JSON.parse(File.read(fn))
	if cfg.has_key?("draft") and cfg["draft"]
		next
	end

	if not cfg.has_key?('slug')
		# Create a string slug (http://stackoverflow.com/questions/4308377/ruby-post-title-to-slug)
		cfg['slug'] = cfg['title'].downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')	
	end

	cfg['filename'] = fn
	cfg['outputfile'] = 'dist/'+cfg['slug']+'.html'

	SOURCES.push(cfg)
	DEPS.push(cfg['outputfile'])
end

SOURCES.sort_by { |hsh| hsh[:zip] }
maxback = -([SOURCES.length, 3].min)
SOURCES.each_with_index do |item, index|
	op = "./generate.py "+item['filename']

	if index > 0
		op += " --previous "+SOURCES[index - 1]['filename']
	end

	if index < (SOURCES.length - 1)
		op += " --next "+SOURCES[index + 1]['filename']
	end
	
	op += " --latest "
	(maxback..-1).each do |n|
		op += SOURCES[n]['filename']
	end

	op += " > "+item['outputfile']

	file item['outputfile'] => ["dist", item['filename']] do
		sh op
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

file "dist/index.html" => DEPS.concat(["dist/js", "dist/images", "dist/css"]) do
	# Just copy the latest post to the index
	sh "cp "+SOURCES[-1]['outputfile']+" dist/index.html"
end

desc "Build."
task :build => ["dist", "dist/index.html"]
