require 'net/ssh'

PAGE_DIR = ENV['PAGE_DIR'] || "#{Dir.pwd}/resources/pages"
PORT = ENV['PORT'] || 5000
NAME = 'xyzy-min'
REPO = 'git@gitlab.com:axocomm/xyzy-min.git'
CONFIG = {
  :staging => {
    :host        => 'www.dev.xyzyxyzy.xyz',
    :user        => 'deploy',
    :remote_path => '/home/deploy/xyzy-min'
  }
}

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

  task :run_docker => [
         'gulp:build',
         'docker:build',
         'docker:run'
       ]
end

task :deploy, [:environment] => 'gulp:build' do |t, args|
  if args.include?(:environment)
    environment = args[:environment].to_sym
  else
    environment = :staging
  end

  unless CONFIG.include?(environment)
    raise "Unknown environment #{environment.to_s}"
  end

  config = CONFIG[environment]
  host = config[:host]
  user = config[:user]
  remote_path = config[:remote_path]
  options = {:verbose => :error}

  cmd = <<-EOT
rsync -rave ssh \
  --exclude='.git/' \
  --exclude='venv/' \
  --exclude='node_modules/' \
  . #{user}@#{host}:#{remote_path}
EOT

  sh cmd

  commands = [
    "cd #{remote_path} && bundle install --deployment",
    "cd #{remote_path} && bundle exec rake docker:build",
    "cd #{remote_path} && bundle exec rake docker:stop",
    "cd #{remote_path} && bundle exec rake docker:rm",
    "cd #{remote_path} && bundle exec rake docker:run"
  ]

  Net::SSH.start(host, user, options) do |ssh|
    commands.each { |c| puts ssh.exec!(c) }
    ssh.loop
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

  task :stop do
    sh "docker stop #{NAME}"
  end

  task :restart => [:stop, :run]

  task :rm, :tag do |t, args| 
    tag = args[:tag] || 'master'
    sh "docker rm #{NAME}"
  end

  task :enter do |t, args|
    sh "docker exec -it #{NAME} bash"
  end
end
