import os
import joblib
PACKAGE_DIR=os.path.dirname(__file__)

class GenderClassifier():
    def __init__(self,name=None):
        #super(GenderClassifier,self).__init__()
        self.name=name

    def __repr__(self):
        return 'GenderClassifier(name={})'.format(self.name)

    def predict(self):
        mz_gender_vectorizer=open(os.path.join(PACKAGE_DIR,'models\mz_gender_vectorizer.pkl'),'rb')
        gender_cv=joblib.load(mz_gender_vectorizer)
        data=gender_cv.transform([self.name]).toarray()

        mz_gender_nv_model=open(os.path.join(PACKAGE_DIR,'models\mz_gender_nv_model.pkl'),'rb')
        gender_clf=joblib.load(mz_gender_nv_model)
        prediction=gender_clf.predict(data)

        if prediction[0]==0:
            result='female'
        elif prediction[0]==1:
            result='male'
        return result
