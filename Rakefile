require 'net/ssh'
require 'yaml'

PORT = (ENV['PORT'] || 5000).freeze
IMAGE_NAME = 'xyzy-min'.freeze
REPO = 'git@gitlab.com:axocomm/xyzy-min.git'.freeze
CONFIG = 'resources/config.yml'.freeze

class Hash
  def symbolize
    self.inject({}) do |acc, (k, v)|
      vv = v.is_a?(Hash) ? v.symbolize : v
      kk = k.to_sym
      acc[kk] = vv
      acc
    end
  end
end

def get_config(environment)
  file = "#{Dir.pwd}/#{CONFIG}"
  raise "#{file} doesn't exist" unless File.exists?(file)
  File.open(file) do |fh|
    conf = YAML.load(fh.read).symbolize
    dc = conf[:deploy] or raise "Missing 'deploy' in configuration"

    raise "Invalid environment #{environment}" unless dc.include?(environment)
    dc[environment]
  end
end

environment = (ENV['ENVIRONMENT'] || 'staging').to_sym
$config = get_config(environment) or raise 'Could not get configuration'

task :default => 'dev:run'

task :dump do
  puts $config.inspect
end

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
      --exclude='__pycache__/' \
      --exclude='node_modules/' \
      . #{user}@#{host}:#{remote_path}
  EOT

  sh cmd

  prefix = "cd #{remote_path} && ENVIRONMENT=#{ENV['ENVIRONMENT']}"

  commands = [
    'bundle install --deployment',
    'bundle exec rake docker:build',
    'bundle exec rake docker:stop',
    'bundle exec rake docker:rm',
    'bundle exec rake docker:run'
  ].map { |c| "#{prefix} #{c}" }

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
      #{user}@#{host}:#{page_dir}/ \
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
    sh "docker rm #{$config[:name]}"
  end

  desc 'Run Bash in container'
  task :enter do |t, args|
    sh "docker exec -it #{$config[:name]} bash"
  end
end
