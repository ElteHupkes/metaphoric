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

# Load a list of posts
SOURCES=FileList['content/*.md'].select { |fn| !(fn =~ /\.draft\.md$/) }.sort!
SOURCES.each do |fn|
	m = /^content\/\d{4}-\d\d-\d\d-\d\d-\d\d(.+)\.md$/.match(fn)
	outputfile
	file outputfile => ["dist", outputfile, "post.mustache"] do
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

desc "Build."
task :build => DEPS.concat(["dist/js", "dist/images", "dist/css/styles.css"])
