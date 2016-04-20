require 'net/ssh'

PORT = ENV['PORT'] || 5000
IMAGE_NAME = 'xyzy-min'
REPO = 'git@gitlab.com:axocomm/xyzy-min.git'
CONFIG = {
  :staging => {
    :host        => 'www.dev.xyzyxyzy.xyz',
    :user        => 'deploy',
    :remote_path => '/home/deploy/xyzy-min-staging',
    :page_dir    => '/home/deploy/xyzy-min-staging/resources/pages',
    :listen_port => 5000,
    :name        => "#{IMAGE_NAME}-staging"
  },
  :prod => {
    :host        => 'www.dev.xyzyxyzy.xyz',
    :user        => 'deploy',
    :remote_path => '/home/deploy/xyzy-min',
    :page_dir    => '/home/deploy/xyzy-min/resources/pages',
    :listen_port => 3000,
    :name        => "#{IMAGE_NAME}"
  }
}

def get_config(environment)
  if not CONFIG.include?(environment)
    raise "Invalid environment #{environment}"
  end

  CONFIG[environment]
end

environment = (ENV['ENVIRONMENT'] || 'staging').to_sym
$config = get_config environment

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
    sh "PAGE_DIR=#{$config[:page_dir]} python -m app"
  end

  task :run_docker => [
         'gulp:build',
         'docker:build',
         'docker:run'
       ]
end

task :deploy => 'gulp:build' do
  host = $config[:host]
  user = $config[:user]
  remote_path = $config[:remote_path]
  options = {:verbose => :error}

  cmd = <<-EOT
rsync -rave ssh \
  --exclude='.git/' \
  --exclude='venv/' \
  --exclude='node_modules/' \
  . #{user}@#{host}:#{remote_path}
EOT

  sh cmd

  prefix = "cd #{remote_path} && ENVIRONMENT=#{ENV['ENVIRONMENT']}"

  commands = [
    "bundle install --deployment",
    "bundle exec rake docker:build",
    "bundle exec rake docker:stop",
    "bundle exec rake docker:rm",
    "bundle exec rake docker:run"
  ].map { |cmd| "#{prefix} #{cmd}" }

  Net::SSH.start(host, user, options) do |ssh|
    commands.each { |c| puts ssh.exec!(c) }
    ssh.loop
  end
end

task :push_pages do
  host = $config[:host]
  user = $config[:user]
  page_dir = $config[:page_dir]

  cmd = <<-EOT
rsync -rave ssh \
  #{Dir.pwd}/resources/pages/ \
  #{user}@#{host}:#{page_dir}
EOT
  sh cmd
end

namespace :docker do
  task :build, :tag do |t, args|
    tag = args[:tag] || 'master'
    cmd = "docker build -t #{IMAGE_NAME}:#{tag} ."
    sh cmd
  end

  task :run, :tag do |t, args|
    tag = args[:tag] || 'master'
    listen_port = $config[:listen_port]
    name = $config[:name]
    page_dir = $config[:page_dir]
    cmd = <<-EOT
docker run \
  -it \
  -p #{listen_port}:#{PORT} \
  -v #{page_dir}:/pages \
  -d \
  --name #{name} #{IMAGE_NAME}:#{tag}
EOT
    sh cmd
  end

  task :stop do
    sh "docker stop #{$config[:name]}"
  end

  task :restart => [:stop, :run]

  task :rm, :tag do |t, args| 
    tag = args[:tag] || 'master'
    sh "docker rm #{$config[:name]}"
  end

  task :enter do |t, args|
    sh "docker exec -it #{$config[:name]} bash"
  end
end
