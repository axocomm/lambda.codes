PAGE_DIR = ENV['PAGE_DIR'] || "#{Dir.pwd}/resources/pages"

task :default => :run_dev

task :gulp_d do
  sh 'gulp d >/tmp/gulp-d.log 2>&1 &'
end

task :kill_gulp do
  sh 'killall gulp'
end

multitask :run_dev => [:gulp_d] do
  sh "PAGE_DIR=#{PAGE_DIR} python -m app"
end
