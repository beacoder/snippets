class StoreController < ApplicationController
  def index
    # [10] update: fetch all products in alphabetical order
    @products = Product.order(:title)
  end
end
