class Movie < ApplicationRecord
    default_scope { order(created_at: :desc) }
    validates :title, presence: { message: 'The movie must have a title' }
  def self.search(pattern)
    # blank? covers both nil and empty string
    # TODO: never return data if we dont have user_id
    if pattern.present?
      where(arel_table[:title].lower.matches("%#{pattern}%".downcase))
    end

  end
end
