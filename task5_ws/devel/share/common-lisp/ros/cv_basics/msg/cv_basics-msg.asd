
(cl:in-package :asdf)

(defsystem "cv_basics-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "aruco_data" :depends-on ("_package_aruco_data"))
    (:file "_package_aruco_data" :depends-on ("_package"))
  ))