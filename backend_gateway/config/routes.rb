Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      post '/questions', to: 'questions#create'
    end
  end
end
