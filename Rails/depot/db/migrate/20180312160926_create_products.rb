class CreateProducts < ActiveRecord::Migration[5.1]
  def change
    create_table :products do |t|
      t.string :title
      t.text :description
      t.string :image_url

      # [1] update: change format of price field
      t.decimal :price, precision: 8, scale: 2

      t.timestamps
    end
  end
end
