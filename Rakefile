PAGE_DIR = ENV['PAGE_DIR'] || "#{Dir.pwd}/resources/pages"
PORT = ENV['PORT'] || 5000
NAME = 'xyzy-min'

task :default => 'dev:run'

namespace :gulp do
  task :build do
    sh 'gulp build'
  end

  task :watch do
    sh 'gulp d >/tmp/gulp-d.log 2>&1 &'
  end

  task :kill do
    sh 'killall gulp'
  end
end

namespace :dev do
  multitask :run => ['gulp:watch'] do
    sh "PAGE_DIR=#{PAGE_DIR} python -m app"
  end
end

namespace :docker do
  task :build, :tag do |t, args|
    tag = args[:tag] || 'master'
    cmd = "docker build -t #{NAME}:#{tag} ."
    sh cmd
  end

  task :run, :tag do |t, args|
    tag = args[:tag] || 'master'
    cmd = <<-EOT
docker run \
  -it \
  -p #{PORT}:#{PORT} \
  -v #{PAGE_DIR}:/pages \
  -d \
  --name #{NAME} #{NAME}:#{tag}
EOT
    sh cmd
  end

  task :enter do |t, args|
    sh "docker exec -it #{NAME} bash"
  end
end
