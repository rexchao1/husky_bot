import pickle

file = open('husky_model.pkl', 'rb')
file1 = pickle.load(file)
data = open('C:/Users/Rex Chao/Desktop\GitHub/bot/husky_compressed_model.pkl', 'wb')
pickle.dump(file1,data)