Rails.application.routes.draw do

  # [9] update: define root path, create store_index_path and store_index_url accessor methods
  root 'store#index', as: 'store_index'

  resources :products
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
