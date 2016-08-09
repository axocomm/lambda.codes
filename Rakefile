require 'net/ssh'

PORT = ENV['PORT'] || 5000
IMAGE_NAME = 'xyzy-min'
REPO = 'git@gitlab.com:axocomm/xyzy-min.git'
CONFIG = {
  :staging => {
    :host        => 'www.dev.xyzyxyzy.xyz',
    :user        => 'deploy',
    :ssh_port    => 2222,
    :remote_path => '/home/deploy/xyzy-min-staging',
    :page_dir    => '/home/deploy/xyzy-min-staging/resources/pages',
    :listen_port => 5000,
    :name        => "#{IMAGE_NAME}-staging"
  },
  :prod => {
    :host        => 'xyzyxyzy.xyz',
    :user        => 'deploy',
    :ssh_port    => 2222,
    :remote_path => '/home/deploy/xyzy-min',
    :page_dir    => '/home/deploy/xyzy-min/resources/pages',
    :listen_port => 3000,
    :name        => "#{IMAGE_NAME}"
  },
  :development => {
    :page_dir => "#{Dir.pwd}/resources/pages"
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
  desc 'Build resources'
  task :build do
    sh 'gulp build'
  end

  desc 'Run gulp d'
  task :watch do
    sh 'gulp d'
  end

  desc 'Try to kill Gulp'
  task :kill do
    sh 'killall gulp'
  end
end

namespace :dev do
  desc 'Start local Flask'
  task :run do
    config = get_config :development
    sh "PAGE_DIR=#{config[:page_dir]} python -m app"
  end

  desc 'Build and run local Docker container'
  task :run_docker => [
         'gulp:build',
         'docker:build',
         'docker:run'
       ]
end

desc 'Deploy to remote Docker container'
task :deploy => 'gulp:build' do
  host = $config[:host]
  user = $config[:user]
  remote_path = $config[:remote_path]
  options = {
    :verbose => :error,
    :port    => $config[:ssh_port]
  }

  cmd = <<-EOT
rsync -rave 'ssh -p#{$config[:ssh_port]}' \
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

desc 'Synchronize current pages to remote'
task :push_pages do
  host = $config[:host]
  user = $config[:user]
  page_dir = $config[:page_dir]

  cmd = <<-EOT
rsync -rave 'ssh -p#{$config[:ssh_port]}' \
  #{Dir.pwd}/resources/pages/ \
  #{user}@#{host}:#{page_dir}
EOT
  sh cmd
end

desc 'Synchronize current pages from remote'
task :pull_pages do
  host = $config[:host]
  user = $config[:user]
  page_dir = $config[:page_dir]

  cmd = <<-EOT
rsync -rave 'ssh -p#{$config[:ssh_port]}' \
  #{user}@#{host}:#{page_dir} \
  #{Dir.pwd}/resources/pages/
EOT
  sh cmd
end

namespace :docker do
  desc 'Build image'
  task :build, :tag do |t, args|
    tag = args[:tag] || 'master'
    cmd = "docker build -t #{IMAGE_NAME}:#{tag} ."
    sh cmd
  end

  desc 'Run container'
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

  desc 'Stop container'
  task :stop do
    sh "docker stop #{$config[:name]}"
  end

  desc 'Restart container'
  task :restart => [:stop, :run]

  desc 'Remove container'
  task :rm, :tag do |t, args|
    tag = args[:tag] || 'master'
    sh "docker rm #{$config[:name]}"
  end

  desc 'Run Bash in container'
  task :enter do |t, args|
    sh "docker exec -it #{$config[:name]} bash"
  end
end
